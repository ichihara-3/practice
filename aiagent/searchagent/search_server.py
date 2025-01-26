from typing import Dict, Any
import time
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Initialize tools with rate limiting wrapper
last_request_time = 0
min_delay = 2  # Minimum delay between requests in seconds

def rate_limited_search(query: str) -> str:
    global last_request_time
    
    current_time = time.time()
    time_since_last_request = current_time - last_request_time
    
    if time_since_last_request < min_delay:
        time.sleep(min_delay - time_since_last_request)
    
    try:
        search_tool = DuckDuckGoSearchRun()
        result = search_tool.run(query)
        last_request_time = time.time()
        return result
    except Exception as e:
        if "Ratelimit" in str(e):
            time.sleep(5)  # Wait longer if we hit the rate limit
            return "Search failed due to rate limit. Please try again in a few seconds."
        raise e

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
    """Execute the search and return the result."""
    try:
        result = agent_executor.invoke({"input": query})
        return {"output": result["output"]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Interactive mode for testing
    print("Search Agent - Enter your queries (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        try:
            query = input("\nEnter search query (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            if not query.strip():
                continue
                
            print("\nSearching...")
            result = search(query)
            
            if "error" in result:
                print("\nError:", result["error"])
            else:
                print("\nResult:", result["output"])
                
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            
    print("\nThank you for using the Search Agent!")
