from typing import Dict, Any
import time
import os
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

from exceptions import RateLimitError, SearchError, ConfigurationError
from logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger('search_server')

# Validate environment variables
if not os.getenv('OPENAI_API_KEY'):
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ConfigurationError("OPENAI_API_KEY not found in environment variables")

# Initialize tools with rate limiting wrapper
last_request_time = 0
min_delay = 2  # Minimum delay between requests in seconds

def rate_limited_search(query: str) -> str:
    """Execute a rate-limited search query.
    
    Args:
        query (str): The search query to execute
        
    Returns:
        str: The search results
        
    Raises:
        RateLimitError: When rate limit is exceeded
        SearchError: When search operation fails
    """
    global last_request_time
    
    current_time = time.time()
    time_since_last_request = current_time - last_request_time
    
    if time_since_last_request < min_delay:
        wait_time = min_delay - time_since_last_request
        logger.info(f"Rate limiting: waiting {wait_time:.2f} seconds")
        time.sleep(wait_time)
    
    try:
        logger.info(f"Executing search query: {query}")
        search_tool = DuckDuckGoSearchRun()
        result = search_tool.run(query)
        last_request_time = time.time()
        logger.info("Search completed successfully")
        return result
    except Exception as e:
        if "Ratelimit" in str(e):
            logger.warning("Rate limit hit, waiting 5 seconds before retry")
            time.sleep(5)
            raise RateLimitError(retry_after=5)
        logger.error(f"Search failed: {str(e)}", exc_info=True)
        raise SearchError(original_error=e)

tools = [
    Tool(
        name="web_search",
        func=rate_limited_search,
        description="Useful for searching information on the internet. Input should be a search query."
    )
]

# Initialize LLM and agent
llm = ChatOpenAI(temperature=0)

# Create prompt template
prompt = PromptTemplate.from_template(
    """You are a helpful search assistant. Answer the following question: {input}
    
    Use the following tools to help you answer the question:
    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin:
    {agent_scratchpad}
    """
)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=2  # Limit iterations to avoid hitting rate limits
)

def search(query: str) -> Dict[str, Any]:
    """Execute the search and return the result.
    
    Args:
        query (str): The user's search query
        
    Returns:
        Dict[str, Any]: A dictionary containing either the search result or error information
    """
    logger.info(f"Processing search request: {query}")
    try:
        result = agent_executor.invoke({"input": query})
        logger.info("Search request completed successfully")
        return {"output": result["output"]}
    except RateLimitError as e:
        logger.warning(f"Rate limit error: {str(e)}")
        return {
            "error": str(e),
            "retry_after": e.retry_after
        }
    except SearchError as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        return {
            "error": str(e),
            "details": str(e.original_error) if e.original_error else None
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {"error": f"An unexpected error occurred: {str(e)}"}

if __name__ == "__main__":
    # Interactive mode for testing
    logger.info("Starting Search Agent in interactive mode")
    print("Search Agent - Enter your queries (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        try:
            query = input("\nEnter search query (or 'quit' to exit): ")
            if query.lower() == 'quit':
                logger.info("User requested to quit")
                break
            if not query.strip():
                continue
                
            print("\nSearching...")
            result = search(query)
            
            if "error" in result:
                error_msg = result["error"]
                if "retry_after" in result:
                    error_msg += f" (retry after {result['retry_after']} seconds)"
                print("\nError:", error_msg)
            else:
                print("\nResult:", result["output"])
                
        except (KeyboardInterrupt, EOFError):
            logger.info("User interrupted the program")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {str(e)}", exc_info=True)
            print(f"\nAn error occurred: {str(e)}")
            
    logger.info("Search Agent shutting down")
    print("\nThank you for using the Search Agent!")
