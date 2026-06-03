import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# Load the .env keys into the process environment
load_dotenv()

# we explicitly check for the presence of the keys
if not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY manquante — vérifie ton fichier .env")
if not os.environ.get("TAVILY_API_KEY"):
    raise RuntimeError("TAVILY_API_KEY manquante — vérifie ton fichier .env")

# --- LLM ---
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# --- Web Search Tool ---
search_tool = TavilySearch(
    max_results=5,
    topic="general",
)