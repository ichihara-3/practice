import os
from dotenv import load_dotenv
from search_server import search
from exceptions import SearchAgentError, ConfigurationError
from logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger('search_client')

# Validate environment variables
if not os.getenv('OPENAI_API_KEY'):
    logger.error("OPENAI_API_KEY not found in environment variables")
    raise ConfigurationError("OPENAI_API_KEY not found in environment variables")

def format_error_message(response: dict) -> str:
    """Format error message from response.
    
    Args:
        response (dict): Response dictionary containing error information
        
    Returns:
        str: Formatted error message
    """
    error_msg = response["error"]
    if "retry_after" in response:
        error_msg += f"\nPlease try again after {response['retry_after']} seconds."
    if "details" in response and response["details"]:
        error_msg += f"\nDetails: {response['details']}"
    return error_msg

def main():
    """Main function for the Search Agent client."""
    logger.info("Starting Search Agent client")
    print("Welcome to the Search Agent! Type 'quit' to exit.")
    
    while True:
        try:
            # Get user input
            user_input = input("\nWhat would you like to search for? > ")
            
            if user_input.lower() == 'quit':
                logger.info("User requested to quit")
                break
                
            if not user_input.strip():
                logger.warning("Empty input received")
                print("Please enter a valid search query.")
                continue
            
            logger.info(f"Processing user query: {user_input}")
            
            # Call the search function
            response = search(user_input)
            
            # Print the response
            if "error" in response:
                error_msg = format_error_message(response)
                logger.error(f"Search error: {error_msg}")
                print(f"\nError: {error_msg}")
            else:
                logger.info("Search completed successfully")
                print("\nSearch Result:")
                print(response["output"])
                
        except SearchAgentError as e:
            logger.error(f"Search agent error: {str(e)}")
            print(f"\nError: {str(e)}")
        except KeyboardInterrupt:
            logger.info("User interrupted the program")
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            print(f"\nAn unexpected error occurred: {str(e)}")
            print("Please try again or contact support if the problem persists.")
    
    logger.info("Search Agent client shutting down")
    print("\nThank you for using the Search Agent!")

if __name__ == "__main__":
    main()
