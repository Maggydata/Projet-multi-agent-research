import os
from dotenv import load_dotenv

# Loads the contents of the .env file into the process's environment variables
load_dotenv()

# Retrieves the keys from the environment
openai_key = os.environ.get("OPENAI_API_KEY")
tavily_key = os.environ.get("TAVILY_API_KEY")

# Checks their presence without ever displaying the complete key
def check(name, value):
    if not value:
        print(f"{name} is missing or empty.")
    else:
        # Only display the first 6 characters to confirm without exposing the key
        print(f"{name} loaded (starts with : {value[:6]}…)")

check("OPENAI_API_KEY", openai_key)
check("TAVILY_API_KEY", tavily_key)