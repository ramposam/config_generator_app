import os
import logging
from pathlib import Path
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from multi_agent_app.db_utils import execute_ecommerce_query, get_ecommerce_tables, get_table_schema

# Configure logging
logger = logging.getLogger(__name__)

# Load schema documentation
def load_ecommerce_schema() -> str:
    """Load E-commerce database schema from markdown file"""
    schema_path = Path(__file__).parent / "ecommerce_agent.md"
    if schema_path.exists():
        with open(schema_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Schema documentation not found"


@tool
def query_ecommerce_database(sql_query: str) -> str:
    """Execute SQL queries on the E-commerce database (ECOMMERCE_DB, SILVER schema).

    🚨 READ ecommerce_agent_sql_guide.md FOR COMPLETE EXAMPLES! 🚨

    CRITICAL QUOTING RULES (MUST FOLLOW EXACTLY):
    ✅ SELECT "total_price" FROM "SILVER"."T_STG_ORDER_ITEMS"
    ❌ SELECT total_price FROM SILVER.T_STG_ORDER_ITEMS
    ❌ SELECT SUM(total_price) - column name MUST have quotes!

    RULE 1: Quote EVERY identifier - schemas, tables, AND columns
    RULE 2: Use EXACT case as defined in database schema (lowercase, uppercase, or camelCase)
    RULE 3: Column names in aggregate functions: SUM("total_price")
    RULE 4: Column names in WHERE/GROUP BY: WHERE "status" = 'completed'
    RULE 5: Column names in JOINs: ON o."order_id" = oi."order_id"

    Column Names (use EXACT case with quotes):
    - T_STG_ORDERS: "order_id", "user_id", "order_date", "amount", "status"
    - T_STG_ORDER_ITEMS: "order_item_id", "order_id", "product_id", "quantity", "unit_price", "total_price"
    - T_STG_PRODUCTS: "product_id", "product_name", "category", "price"
    - T_STG_USERS: "user_id", "user_name", "email", "country"
    - T_STG_REVIEWS: "review_id", "product_id", "user_id", "rating"
    - T_STG_EVENTS: "event_id", "user_id", "event_type", "product_id"

    ✅ CORRECT Examples:
    - SELECT SUM("total_price") FROM "SILVER"."T_STG_ORDER_ITEMS"
    - SELECT "category", COUNT(*) FROM "SILVER"."T_STG_PRODUCTS" GROUP BY "category"
    - SELECT u."user_name", SUM(oi."total_price") FROM "SILVER"."T_STG_USERS" u JOIN "SILVER"."T_STG_ORDERS" o ON u."user_id" = o."user_id" JOIN "SILVER"."T_STG_ORDER_ITEMS" oi ON o."order_id" = oi."order_id" GROUP BY u."user_name"

    Args:
        sql_query: SQL query (MUST have ALL identifiers quoted!)

    Returns:
        Query results as formatted string
    """
    logger.info(f"Executing E-commerce database query: {sql_query[:100]}...")
    try:
        result = execute_ecommerce_query(sql_query)
        if "error" in result.columns:
            logger.error(f"Query execution failed: {result['error'].iloc[0]}")
            return f"Error executing query: {result['error'].iloc[0]}"
        logger.info("Query executed successfully")
        return result.to_string(index=False, max_rows=50)
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return f"Error executing query: {str(e)}"


@tool
def get_ecommerce_schema_info(table_name: str = None) -> str:
    """Get schema information for E-commerce database tables.
    If table_name is provided, returns schema for that specific table.
    Otherwise, lists all available tables.
    
    Args:
        table_name: Optional table name to get specific schema
        
    Returns:
        Schema information as a formatted string
    """
    try:
        if table_name:
            schema = get_table_schema("ecommerce", table_name)
            return f"Schema for SILVER.{table_name}:\n{schema}"
        else:
            tables = get_ecommerce_tables()
            return f"Available tables in ECOMMERCE_DB.SILVER:\n" + "\n".join([f"- SILVER.{table}" for table in tables])
    except Exception as e:
        return f"Error getting schema info: {str(e)}"


@tool
def get_ecommerce_insights(business_question: str) -> str:
    """Generate insights about e-commerce data by analyzing the database.

    This tool will automatically generate and execute appropriate SQL queries with proper formatting.

    IMPORTANT: This tool generates SQL queries following these rules:
    - ALL column names are wrapped in double quotes with exact case
    - ALL table names are wrapped in double quotes
    - ALL schema names are wrapped in double quotes
    - Example: SELECT SUM("total_price") FROM "SILVER"."T_STG_ORDER_ITEMS"

    Supported analyses:
    - Revenue/Sales analysis
    - Product reviews and ratings
    - Product information
    - User/Customer analysis

    Args:
        business_question: A natural language question about the e-commerce data
        
    Returns:
        Analysis results as a formatted string
    """
    try:
        # Common business queries
        question_lower = business_question.lower()
        
        if "revenue" in question_lower or "sales" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_orders,
                    SUM(amount) as total_revenue,
                    AVG(amount) as avg_order_value
                FROM SILVER.T_STG_ORDERS
                WHERE amount IS NOT NULL
            """
            result = execute_ecommerce_query(query)
            return f"Revenue Analysis:\n{result.to_string(index=False)}"
        
        elif "review" in question_lower or "rating" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_reviews,
                    AVG(rating) as avg_rating,
                    MIN(rating) as min_rating,
                    MAX(rating) as max_rating
                FROM SILVER.T_STG_REVIEWS
                WHERE rating IS NOT NULL
            """
            result = execute_ecommerce_query(query)
            return f"Review Analysis:\n{result.to_string(index=False)}"
        
        elif "product" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_products,
                    COUNT(DISTINCT category) as unique_categories
                FROM SILVER.T_STG_PRODUCTS
            """
            result = execute_ecommerce_query(query)
            return f"Product Analysis:\n{result.to_string(index=False)}"
        
        elif "user" in question_lower or "customer" in question_lower:
            query = """
                SELECT 
                    COUNT(*) as total_users,
                    COUNT(DISTINCT country) as countries_represented
                FROM SILVER.T_STG_USERS
            """
            result = execute_ecommerce_query(query)
            return f"User Analysis:\n{result.to_string(index=False)}"
        
        else:
            return "Please specify what you want to analyze (revenue, reviews, products, users, etc.)"
            
    except Exception as e:
        return f"Error generating insights: {str(e)}"


def create_ecommerce_agent(use_groq: bool = False):
    """Create an E-commerce database agent with schema context"""
    logger.info(f"Creating E-commerce agent with use_groq={use_groq}")
    
    # Load schema documentation for logging purposes
    schema_doc = load_ecommerce_schema()
    logger.debug("E-commerce schema documentation loaded")

    # Choose LLM
    if use_groq:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY")
        )
        logger.info("E-commerce agent using Groq llama-3.3-70b-versatile")
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("E-commerce agent using OpenAI gpt-4o-mini")

    # Tools with detailed schema descriptions
    tools = [query_ecommerce_database, get_ecommerce_schema_info, get_ecommerce_insights]

    # Create agent using LangGraph
    agent = create_react_agent(llm, tools)
    logger.info("E-commerce agent created successfully with schema-aware tools")

    return agent
