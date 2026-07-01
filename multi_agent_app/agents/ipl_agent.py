import os
import logging
from pathlib import Path
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from multi_agent_app.db_utils import execute_football_query, get_football_tables, get_table_schema

# Configure logging
logger = logging.getLogger(__name__)

# Load schema documentation
def load_ipl_schema() -> str:
    """Load IPL database schema from markdown file"""
    schema_path = Path(__file__).parent / "ipl_agent.md"
    if schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Schema documentation not found"


@tool
def query_ipl_database(sql_query: str) -> str:
    """Execute SQL queries on the IPL Cricket database (ETL_PIPELINES_DB, SILVER schema).

    🚨 READ ipl_agent.md FOR COMPLETE EXAMPLES! 🚨

    CRITICAL QUOTING RULES (MUST FOLLOW EXACTLY):
    ✅ SELECT "MATCH_ID" FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
    ❌ SELECT MATCH_ID FROM SILVER.T_STG_CRICKET_LEAGUE_IPL_DATA
    ❌ SELECT SUM(RUNS_OF_BAT) - column name MUST have quotes!

    RULE 1: Quote EVERY identifier - schemas, tables, AND columns
    RULE 2: Use EXACT case as defined in database schema (UPPERCASE)
    RULE 3: Column names in aggregate functions: SUM("RUNS_OF_BAT")
    RULE 4: Column names in WHERE/GROUP BY: WHERE "BATTING_TEAM" = 'Mumbai Indians'
    RULE 5: Column names in JOINs: ON i."MATCH_ID" = i2."MATCH_ID"

    Column Names (use EXACT case with quotes):
    - T_STG_CRICKET_LEAGUE_IPL_DATA: "MATCH_ID", "SEASON", "MATCH_NO", "DATE", "VENUE", 
      "BATTING_TEAM", "BOWLING_TEAM", "INNINGS", "OVER", "STRIKER", "BOWLER", 
      "RUNS_OF_BAT", "EXTRAS", "WIDE", "LEGBYES", "BYES", "NOBALLS", 
      "WICKET_TYPE", "PLAYER_DISMISSED", "FIELDER"

    ✅ CORRECT Examples:
    - SELECT COUNT(*) FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
    - SELECT SUM("RUNS_OF_BAT") FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
    - SELECT "STRIKER", SUM("RUNS_OF_BAT") FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA" GROUP BY "STRIKER"
    - SELECT "SEASON", "BATTING_TEAM", SUM("RUNS_OF_BAT") FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA" GROUP BY "SEASON", "BATTING_TEAM"

    Args:
        sql_query: SQL query (MUST have ALL identifiers quoted!)

    Returns:
        Query results as formatted string
    """
    logger.info(f"[TOOL CALL] query_ipl_database called with query: {sql_query[:200]}...")
    try:
        result = execute_football_query(sql_query)
        if "error" in result.columns:
            logger.error(f"[TOOL ERROR] Query execution failed: {result['error'].iloc[0]}")
            return f"Error executing query: {result['error'].iloc[0]}"
        logger.info(f"[TOOL SUCCESS] Query executed successfully. Result rows: {len(result)}")
        return result.to_string(index=False, max_rows=50)
    except Exception as e:
        logger.error(f"[TOOL ERROR] Exception during query execution: {str(e)}")
        return f"Error executing query: {str(e)}"


@tool
def get_ipl_schema_info(table_name: str = None) -> str:
    """Get schema information for IPL database tables.
    If table_name is provided, returns schema for that specific table.
    Otherwise, lists all available tables.
    
    Args:
        table_name: Optional table name to get specific schema
        
    Returns:
        Schema information as a formatted string
    """
    logger.info(f"[TOOL CALL] get_ipl_schema_info called with table_name: {table_name}")
    try:
        if table_name:
            schema = get_table_schema("ipl", table_name)
            logger.info(f"[TOOL SUCCESS] Schema retrieved for {table_name}")
            return f"Schema for SILVER.{table_name}:\n{schema}"
        else:
            logger.info("[TOOL SUCCESS] Listed all available tables")
            return f"Available tables in ETL_PIPELINES_DB.SILVER:\n- SILVER.T_STG_CRICKET_LEAGUE_IPL_DATA"
    except Exception as e:
        logger.error(f"[TOOL ERROR] Exception getting schema info: {str(e)}")
        return f"Error getting schema info: {str(e)}"


@tool
def get_ipl_insights(business_question: str) -> str:
    """Generate insights about IPL cricket data by analyzing the database.

    This tool will automatically generate and execute appropriate SQL queries with proper formatting.

    IMPORTANT: This tool generates SQL queries following these rules:
    - ALL column names are wrapped in double quotes with exact case (UPPERCASE)
    - ALL table names are wrapped in double quotes
    - ALL schema names are wrapped in double quotes
    - Example: SELECT "STRIKER", SUM("RUNS_OF_BAT") FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"

    Supported analyses:
    - Season-wise statistics (runs, wickets, matches)
    - Team performance analysis
    - Player statistics (batsmen and bowlers)
    - Venue analysis
    - Dismissal types analysis
    - Over-wise analysis (powerplay, death overs)

    Args:
        business_question: A natural language question about the IPL data
        
    Returns:
        Analysis results as a formatted string
    """
    logger.info(f"[TOOL CALL] get_ipl_insights called with question: {business_question[:200]}...")
    try:
        # Common IPL queries
        question_lower = business_question.lower()
        
        if "season" in question_lower:
            logger.info("[TOOL LOG] Executing season-wise analysis query")
            query = """
                SELECT 
                    "SEASON",
                    COUNT(DISTINCT "MATCH_ID") as total_matches,
                    SUM("RUNS_OF_BAT") as total_runs,
                    COUNT("WICKET_TYPE") as total_wickets
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                GROUP BY "SEASON"
                ORDER BY "SEASON"
            """
            result = execute_football_query(query)
            logger.info(f"[TOOL SUCCESS] Season analysis completed. Rows: {len(result)}")
            return f"Season-wise Analysis:\n{result.to_string(index=False)}"
        
        elif "team" in question_lower:
            query = """
                SELECT 
                    "BATTING_TEAM",
                    COUNT(DISTINCT "MATCH_ID") as matches_played,
                    SUM("RUNS_OF_BAT") as total_runs,
                    COUNT("WICKET_TYPE") as wickets_lost
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                GROUP BY "BATTING_TEAM"
                ORDER BY total_runs DESC
            """
            result = execute_football_query(query)
            return f"Team Performance Analysis:\n{result.to_string(index=False)}"
        
        elif "batsman" in question_lower or "run" in question_lower or "striker" in question_lower:
            query = """
                SELECT 
                    "STRIKER",
                    COUNT(*) as balls_faced,
                    SUM("RUNS_OF_BAT") as total_runs,
                    COUNT(CASE WHEN "RUNS_OF_BAT" = 4 THEN 1 END) as fours,
                    COUNT(CASE WHEN "RUNS_OF_BAT" = 6 THEN 1 END) as sixes,
                    ROUND(SUM("RUNS_OF_BAT")::numeric / NULLIF(COUNT(*), 0), 2) as strike_rate
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                GROUP BY "STRIKER"
                ORDER BY total_runs DESC
                LIMIT 20
            """
            result = execute_football_query(query)
            return f"Top Batsmen Analysis:\n{result.to_string(index=False)}"
        
        elif "bowler" in question_lower or "wicket" in question_lower:
            query = """
                SELECT 
                    "BOWLER",
                    COUNT(*) as balls_bowled,
                    SUM("RUNS_OF_BAT") + SUM("EXTRAS") as runs_conceded,
                    COUNT("WICKET_TYPE") as wickets
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                GROUP BY "BOWLER"
                HAVING COUNT("WICKET_TYPE") > 0
                ORDER BY wickets DESC
                LIMIT 20
            """
            result = execute_football_query(query)
            return f"Top Bowlers Analysis:\n{result.to_string(index=False)}"
        
        elif "venue" in question_lower or "stadium" in question_lower:
            query = """
                SELECT 
                    "VENUE",
                    COUNT(DISTINCT "MATCH_ID") as matches_played,
                    SUM("RUNS_OF_BAT") as total_runs,
                    ROUND(AVG("RUNS_OF_BAT"), 2) as avg_runs_per_ball
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                GROUP BY "VENUE"
                ORDER BY matches_played DESC
            """
            result = execute_football_query(query)
            return f"Venue Analysis:\n{result.to_string(index=False)}"
        
        elif "dismissal" in question_lower or "wicket type" in question_lower:
            query = """
                SELECT 
                    "WICKET_TYPE",
                    COUNT(*) as count,
                    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                WHERE "WICKET_TYPE" IS NOT NULL
                GROUP BY "WICKET_TYPE"
                ORDER BY count DESC
            """
            result = execute_football_query(query)
            return f"Dismissal Types Analysis:\n{result.to_string(index=False)}"
        
        elif "powerplay" in question_lower:
            query = """
                SELECT 
                    "SEASON",
                    "BATTING_TEAM",
                    SUM("RUNS_OF_BAT") + SUM("EXTRAS") as powerplay_runs,
                    COUNT("WICKET_TYPE") as powerplay_wickets
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                WHERE "OVER" < 6
                GROUP BY "SEASON", "BATTING_TEAM"
                ORDER BY "SEASON", powerplay_runs DESC
            """
            result = execute_football_query(query)
            return f"Powerplay Analysis:\n{result.to_string(index=False)}"
        
        elif "death" in question_lower:
            query = """
                SELECT 
                    "SEASON",
                    "BATTING_TEAM",
                    SUM("RUNS_OF_BAT") + SUM("EXTRAS") as death_overs_runs,
                    COUNT("WICKET_TYPE") as death_overs_wickets
                FROM "SILVER"."T_STG_CRICKET_LEAGUE_IPL_DATA"
                WHERE "OVER" >= 16
                GROUP BY "SEASON", "BATTING_TEAM"
                ORDER BY "SEASON", death_overs_runs DESC
            """
            result = execute_football_query(query)
            return f"Death Overs Analysis:\n{result.to_string(index=False)}"
        
        else:
            logger.warning("[TOOL WARNING] No matching analysis pattern found")
            return "Please specify what you want to analyze (season, team, batsman, bowler, venue, dismissal types, powerplay, death overs, etc.)"
            
    except Exception as e:
        logger.error(f"[TOOL ERROR] Exception generating insights: {str(e)}")
        return f"Error generating insights: {str(e)}"


def create_ipl_agent(use_groq: bool = False):
    """Create an IPL Cricket database agent with schema context"""
    logger.info(f"Creating IPL agent with use_groq={use_groq}")
    
    # Load schema documentation for logging purposes
    schema_doc = load_ipl_schema()
    logger.debug("IPL schema documentation loaded")

    # Choose LLM
    if use_groq:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("IPL agent using Groq llama-3.3-70b-versatile")
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("IPL agent using OpenAI gpt-4o-mini")

    # Tools with detailed schema descriptions
    tools = [query_ipl_database, get_ipl_schema_info, get_ipl_insights]

    # Create agent using LangGraph
    agent = create_agent(llm, tools)
    logger.info("IPL agent created successfully with schema-aware tools")

    return agent
