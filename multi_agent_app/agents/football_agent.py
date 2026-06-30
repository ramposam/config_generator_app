import os
import logging
from pathlib import Path
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from multi_agent_app.db_utils import execute_football_query, get_football_tables, get_table_schema

# Configure logging
logger = logging.getLogger(__name__)

# Load schema documentation
def load_football_schema() -> str:
    """Load Football database schema from markdown file"""
    schema_path = Path(__file__).parent / "football_agent.md"
    if schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Schema documentation not found"


@tool
def query_football_database(sql_query: str) -> str:
    """Execute SQL queries on the Football database (ETL_PIPELINES_DB, public schema).

    🚨 READ football_agent_sql_guide.md FOR COMPLETE EXAMPLES! 🚨

    CRITICAL QUOTING RULES (MUST FOLLOW EXACTLY):
    ✅ SELECT "overall_rating" FROM "public"."PLAYER_ATTRIBUTES"
    ❌ SELECT overall_rating FROM public.PLAYER_ATTRIBUTES
    ❌ SELECT AVG(overall_rating) - column name MUST have quotes!

    RULE 1: Quote EVERY identifier - schemas, tables, AND columns
    RULE 2: Use EXACT case as defined in database schema (lowercase, uppercase, or camelCase)
    RULE 3: camelCase columns like: "buildUpPlaySpeed", "defenseAggression"
    RULE 4: Column names in aggregate functions: AVG("overall_rating")
    RULE 5: Column names in WHERE/GROUP BY: WHERE "position" = 'Forward'
    RULE 6: Column names in JOINs: ON p."player_id" = pa."player_id"

    Column Names (use EXACT case with quotes):
    - PLAYER: "player_id", "player_name", "nationality", "position"
    - MATCH: "match_id", "home_team_goal", "away_team_goal", "match_date"
    - TEAM: "team_id", "team_short_name", "team_long_name"
    - LEAGUE: "league_id", "league_name", "country_id"
    - COUNTRY: "country_id", "country_name"
    - PLAYER_ATTRIBUTES: "player_id", "overall_rating", "potential", "pace", "shooting"
    - TEAM_ATTRIBUTES: "team_id", "buildUpPlaySpeed", "defenseAggression" (camelCase!)

    ✅ CORRECT Examples:
    - SELECT COUNT(*) FROM "public"."PLAYER"
    - SELECT SUM(CASE WHEN "home_team_goal" > "away_team_goal" THEN 1 ELSE 0 END) FROM "public"."MATCH"
    - SELECT "player_name", "overall_rating" FROM "public"."PLAYER" p JOIN "public"."PLAYER_ATTRIBUTES" pa ON p."player_id" = pa."player_id"

    Args:
        sql_query: SQL query (MUST have ALL identifiers quoted!)

    Returns:
        Query results as formatted string
    """
    logger.info(f"Executing Football database query: {sql_query[:100]}...")
    try:
        result = execute_football_query(sql_query)
        if "error" in result.columns:
            logger.error(f"Query execution failed: {result['error'].iloc[0]}")
            return f"Error executing query: {result['error'].iloc[0]}"
        logger.info("Query executed successfully")
        return result.to_string(index=False, max_rows=50)
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return f"Error executing query: {str(e)}"


@tool
def get_football_schema_info(table_name: str = None) -> str:
    """Get schema information for Football database tables.
    If table_name is provided, returns schema for that specific table.
    Otherwise, lists all available tables.
    
    Args:
        table_name: Optional table name to get specific schema
        
    Returns:
        Schema information as a formatted string
    """
    try:
        if table_name:
            schema = get_table_schema("football", table_name)
            return f"Schema for public.{table_name}:\n{schema}"
        else:
            tables = get_football_tables()
            return f"Available tables in ETL_PIPELINES_DB.public:\n" + "\n".join([f"- public.{table}" for table in tables])
    except Exception as e:
        return f"Error getting schema info: {str(e)}"


@tool
def get_football_insights(business_question: str) -> str:
    """Generate insights about football data by analyzing the database.

    This tool will automatically generate and execute appropriate SQL queries with proper formatting.

    IMPORTANT: This tool generates SQL queries following these rules:
    - ALL column names are wrapped in double quotes with exact case
    - ALL table names are wrapped in double quotes
    - ALL schema names are wrapped in double quotes
    - Example: SELECT "player_name", "overall_rating" FROM "public"."PLAYER"

    Supported analyses:
    - Player information and statistics
    - Match statistics and results
    - Team information and performance
    - League information
    - Country information

    Args:
        business_question: A natural language question about the football data
        
    Returns:
        Analysis results as a formatted string
    """
    try:
        # Common football queries
        question_lower = business_question.lower()
        
        if "player" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_players,
                    COUNT(DISTINCT nationality) as countries_represented
                FROM PLAYER
            """
            result = execute_football_query(query)
            return f"Player Analysis:\n{result.to_string(index=False)}"
        
        elif "match" in question_lower or "game" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_matches,
                    SUM(CASE WHEN home_team_goal > away_team_goal THEN 1 ELSE 0 END) as home_wins,
                    SUM(CASE WHEN home_team_goal < away_team_goal THEN 1 ELSE 0 END) as away_wins,
                    SUM(CASE WHEN home_team_goal = away_team_goal THEN 1 ELSE 0 END) as draws
                FROM MATCH
            """
            result = execute_football_query(query)
            return f"Match Analysis:\n{result.to_string(index=False)}"
        
        elif "team" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_teams,
                    COUNT(DISTINCT team_long_name) as unique_team_names
                FROM TEAM
            """
            result = execute_football_query(query)
            return f"Team Analysis:\n{result.to_string(index=False)}"
        
        elif "league" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_leagues,
                    COUNT(DISTINCT country_id) as countries
                FROM LEAGUE
            """
            result = execute_football_query(query)
            return f"League Analysis:\n{result.to_string(index=False)}"
        
        elif "country" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_countries
                FROM COUNTRY
            """
            result = execute_football_query(query)
            return f"Country Analysis:\n{result.to_string(index=False)}"
        
        else:
            return "Please specify what you want to analyze (players, matches, teams, leagues, countries, etc.)"
            
    except Exception as e:
        return f"Error generating insights: {str(e)}"


def create_football_agent(use_groq: bool = False):
    """Create a Football database agent with schema context"""
    logger.info(f"Creating Football agent with use_groq={use_groq}")
    
    # Load schema documentation for logging purposes
    schema_doc = load_football_schema()
    logger.debug("Football schema documentation loaded")

    # Choose LLM
    if use_groq:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("Football agent using Groq llama-3.3-70b-versatile")
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("Football agent using OpenAI gpt-4o-mini")

    # Tools with detailed schema descriptions
    tools = [query_football_database, get_football_schema_info, get_football_insights]

    # Create agent using LangGraph
    agent = create_react_agent(llm, tools)
    logger.info("Football agent created successfully with schema-aware tools")

    return agent
