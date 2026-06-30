import sqlite3
import os
import pandas as pd
from sqlalchemy import create_engine, text

# PostgreSQL connection parameters - update these with your actual credentials
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ETL_PIPELINES_DB"
DB_USER = os.getenv("DB_USER", "etl_pipeline")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# SQLite source database
SQLITE_DB_PATH = r"C:\Users\Asus\Downloads\database.sqlite"

def main():
    # Connect to SQLite source database
    sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Get all table names from SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    print("Tables in SQLite database:", tables)
    
    # Connect to PostgreSQL destination database
    pg_engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    pg_conn = pg_engine.connect()
    
    for table in tables:
        original_table_name = table[0]
        uppercase_table_name = original_table_name.upper()
        
        print(f"\nProcessing table: {original_table_name} -> {uppercase_table_name}")
        
        # Read data from SQLite table
        df = pd.read_sql(f"SELECT * FROM {original_table_name};", sqlite_conn)
        print(f"Original columns: {list(df.columns)}")
        
        # Convert column names to uppercase
        df.columns = [col.upper() for col in df.columns]
        print(f"Uppercase columns: {list(df.columns)}")
        print(f"Data shape: {df.shape}")
        print(df.head(10))
        
        # Drop table if it exists in PostgreSQL
        try:
            pg_conn.execute(text(f"DROP TABLE IF EXISTS {uppercase_table_name};"))
            pg_conn.commit()
            print(f"Dropped existing table {uppercase_table_name} if it existed")
        except Exception as e:
            print(f"Error dropping table: {e}")
        
        # Create table in PostgreSQL with uppercase names
        try:
            # Write DataFrame to PostgreSQL with uppercase table name
            df.to_sql(
                uppercase_table_name,
                pg_engine,
                if_exists='replace',
                index=False
            )
            print(f"Successfully created table {uppercase_table_name} in PostgreSQL")
        except Exception as e:
            print(f"Error creating table {uppercase_table_name}: {e}")
    
    # Close connections
    sqlite_conn.close()
    pg_conn.close()
    print("\nMigration completed successfully!")

if __name__ == "__main__":
    main()
