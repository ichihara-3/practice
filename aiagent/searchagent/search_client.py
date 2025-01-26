import os
from dotenv import load_dotenv
from search_server import search

load_dotenv()

def main():
    print("Welcome to the Search Agent! Type 'quit' to exit.")
    
    while True:
        # Get user input
        user_input = input("\nWhat would you like to search for? > ")
        
        if user_input.lower() == 'quit':
            break
            
        try:
            # Call the search function
            response = search(user_input)
            
            # Print the response
            if "error" in response:
                print(f"Error: {response['error']}")
            else:
                print("\nSearch Result:")
                print(response["output"])
                
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
