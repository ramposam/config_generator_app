import os
import logging
from pathlib import Path
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tavily import TavilyClient

# Configure logging
logger = logging.getLogger(__name__)

# Load schema documentation
def load_tavily_schema() -> str:
    """Load Tavily search agent schema from markdown file"""
    schema_path = Path(__file__).parent / "tavily_agent.md"
    if schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Schema documentation not found"


@tool
def search_web(query: str) -> str:
    """Search the web for information using Tavily AI Search API.

    IMPORTANT: Review schema documentation for complete search guidance.

    Best for:
    - General web searches with natural language queries
    - News and current events
    - Research topics and trends
    - Company and product information
    - Technology updates
    - Latest developments

    Search Parameters:
    - query (required): Natural language search query
      Example: "latest AI trends 2024"
      Example: "Python best practices"
      Example: "COVID vaccine updates"

    API Details:
    - Service: Tavily AI Search
    - Max results: 5 per query
    - Search depth: basic (global web)
    - Response format: Title, URL, Content (500 chars max)

    Tips for Better Results:
    - Be specific in queries (narrow = better results)
    - Use keywords naturally
    - Include context for relevant filtering
    - Great for time-sensitive information

    Example Response:
    Title: Article Title
    URL: https://example.com/article
    Content: First 500 characters of article...

    Args:
        query: The search query string
        
    Returns:
        Search results as a formatted string with title, URL, and content
    """
    logger.info(f"Searching web for: {query}")
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = tavily_client.search(query=query, search_depth="basic", max_results=5)
        
        results = []
        for result in response.get("results", []):
            results.append(f"Title: {result.get('title', 'N/A')}")
            results.append(f"URL: {result.get('url', 'N/A')}")
            results.append(f"Content: {result.get('content', 'N/A')[:500]}...")
            results.append("---")
        
        return "\n".join(results) if results else "No results found"
    except Exception as e:
        logger.error(f"Error searching web: {str(e)}")
        return f"Error searching web: {str(e)}"


def create_tavily_agent(use_groq: bool = False):
    """Create a Tavily web search agent with schema context"""
    logger.info(f"Creating Tavily agent with use_groq={use_groq}")
    
    # Load schema documentation for logging purposes
    schema_doc = load_tavily_schema()
    logger.debug("Tavily search schema documentation loaded")

    # Choose LLM
    if use_groq:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("Tavily agent using Groq llama-3.3-70b-versatile")
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("Tavily agent using OpenAI gpt-4o-mini")
    
    # Tools with detailed API descriptions
    tools = [search_web]
    
    # Create agent using LangGraph
    agent = create_react_agent(llm, tools)
    logger.info("Tavily agent created successfully with schema-aware tools")

    return agent
