import psycopg2
import psycopg2.errors
import re
import sqlparse

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "etl_pipeline"
DB_PASSWORD = "etl_pipeline"
SQL_FILE = "ddl.sql"


def connect(dbname="postgres"):
    return psycopg2.connect(
        dbname=dbname,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def rewrite_cross_db_references(sql: str) -> str:
    """
    Convert:
        "DB"."SCHEMA"."TABLE"
    into:
        "SCHEMA"."TABLE"
    """

    pattern = r'"([^"]+)"\."([^"]+)"\."([^"]+)"'

    return re.sub(
        pattern,
        lambda m: f'"{m.group(2)}"."{m.group(3)}"',
        sql,
    )


def get_create_database_name(cmd):
    m = re.match(
        r'CREATE\s+DATABASE(?:\s+IF\s+NOT\s+EXISTS)?\s+"?([^"]+)"?',
        cmd,
        re.IGNORECASE,
    )
    return m.group(1) if m else None


def get_use_database_name(cmd):
    m = re.match(
        r'USE(?:\s+DATABASE)?\s+"?([^"]+)"?',
        cmd,
        re.IGNORECASE,
    )
    return m.group(1) if m else None


def execute_sql_file():

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql_commands = sqlparse.split(f.read())

    conn = connect("postgres")
    conn.autocommit = True
    cur = conn.cursor()

    current_db = "postgres"

    for command in sql_commands:

        cmd = command.strip()

        if not cmd:
            continue

        cmd = rewrite_cross_db_references(cmd)

        try:

            ##################################################
            # CREATE DATABASE
            ##################################################
            dbname = get_create_database_name(cmd)

            if dbname:

                try:
                    cur.execute(f'CREATE DATABASE "{dbname}"')
                    print(f"Database created : {dbname}")

                except psycopg2.errors.DuplicateDatabase:
                    print(f"Database already exists : {dbname}")

                # Automatically connect to the new database
                cur.close()
                conn.close()

                conn = connect(dbname)
                conn.autocommit = True
                cur = conn.cursor()

                current_db = dbname

                print(f"Connected to {dbname}")

                continue

            ##################################################
            # USE DATABASE
            ##################################################
            dbname = get_use_database_name(cmd)

            if dbname:

                cur.close()
                conn.close()

                conn = connect(dbname)
                conn.autocommit = True
                cur = conn.cursor()

                current_db = dbname

                print(f"Switched to {dbname}")

                continue

            ##################################################
            # Execute SQL
            ##################################################
            cur.execute(cmd)
            print(f"{cmd} Executed Successfully")

            print(f"[{current_db}] Executed")

        except Exception as e:

            print("\n-----------------------------")
            print(f"Database : {current_db}")
            print("SQL:")
            print(cmd)
            print("\nERROR:")
            print(e)
            print("-----------------------------\n")

    cur.close()
    conn.close()


if __name__ == "__main__":
    execute_sql_file()