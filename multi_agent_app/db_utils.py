import os
import logging
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database URLs
FOOTBALL_DB_URL = os.getenv("POSTGRES_DB_URL", "postgresql://etl_pipeline:etl_pipeline@localhost:5432/ETL_PIPELINES_DB")
ECOMMERCE_DB_URL = os.getenv("ECOMMERCE_DB_URL", "postgresql://etl_pipeline:etl_pipeline@localhost:5432/ECOMMERCE_DB")

# Create engines
football_engine = create_engine(FOOTBALL_DB_URL)
ecommerce_engine = create_engine(ECOMMERCE_DB_URL)

# Create session factories
FootballSessionLocal = sessionmaker(bind=football_engine)
EcommerceSessionLocal = sessionmaker(bind=ecommerce_engine)


def execute_football_query(query: str) -> pd.DataFrame:
    """Execute a query on the football database (ETL_PIPELINES_DB, public schema)"""
    logger.info(f"Executing football database query (first 200 chars): {query[:200]}...")
    start_time = time.time()
    try:
        with football_engine.connect() as conn:
            result = pd.read_sql_query(text(query), conn)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"Football query executed successfully in {duration:.2f} seconds")
        logger.info(f"Result rows: {len(result)}, columns: {len(result.columns)}")
        return result
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"Football query failed after {duration:.2f} seconds: {str(e)}")
        return pd.DataFrame({"error": [str(e)]})


def execute_ecommerce_query(query: str) -> pd.DataFrame:
    """Execute a query on the e-commerce database (ECOMMERCE_DB, SILVER schema)"""
    logger.info(f"Executing e-commerce database query (first 200 chars): {query[:200]}...")
    start_time = time.time()
    try:
        with ecommerce_engine.connect() as conn:
            result = pd.read_sql_query(text(query), conn)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"E-commerce query executed successfully in {duration:.2f} seconds")
        logger.info(f"Result rows: {len(result)}, columns: {len(result.columns)}")
        return result
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(f"E-commerce query failed after {duration:.2f} seconds: {str(e)}")
        return pd.DataFrame({"error": [str(e)]})


def get_football_tables() -> list:
    """Get list of tables in football database"""
    tables = [
        "PLAYER", "MATCH", "LEAGUE", "TEAM", "COUNTRY",
        "TEAM_ATTRIBUTES", "PLAYER_ATTRIBUTES"
    ]
    return tables


def get_ecommerce_tables() -> list:
    """Get list of tables in e-commerce database"""
    tables = [
        "T_STG_ORDERS", "T_STG_REVIEWS", "T_STG_EVENTS",
        "T_STG_ORDER_ITEMS", "T_STG_PRODUCTS", "T_STG_USERS"
    ]
    return tables


def get_ipl_tables() -> list:
    """Get list of tables in IPL database"""
    tables = [
        "T_STG_CRICKET_LEAGUE_IPL_DATA"
    ]
    return tables


def get_table_schema(database: str, table: str) -> str:
    """Get schema information for a table"""
    logger.info(f"Getting schema for {database}.{table}")
    if database == "football":
        query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = '{table}'
            ORDER BY ordinal_position;
        """
        result = execute_football_query(query)
    elif database == "ecommerce":
        query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'SILVER' AND table_name = '{table}'
            ORDER BY ordinal_position;
        """
        result = execute_ecommerce_query(query)
    elif database == "ipl":
        query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'SILVER' AND table_name = '{table}'
            ORDER BY ordinal_position;
        """
        result = execute_football_query(query)
    else:
        logger.warning(f"Invalid database: {database}")
        return "Invalid database"
    
    if not result.empty and "error" not in result.columns:
        logger.info(f"Schema retrieved successfully for {database}.{table}")
        return result.to_string(index=False)
    logger.warning(f"No schema information found for {database}.{table}")
    return "No schema information found"
