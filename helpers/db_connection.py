import snowflake.connector
from threading import Lock


class SnowflakeSingleton:

    _instance = None
    _lock = Lock()  # Ensures thread-safe singleton


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SnowflakeSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_connection"):
            self._connection = None

    def connect(self, user, password, account, database, schema,warehouse,role):
        """
        Establish a connection to Snowflake. If already connected, reuse the existing connection.
        """
        if not self._connection:
            self._connection = snowflake.connector.connect(
                user=user,
                password=password,
                account=account,
                database=database,
                schema=schema,
                warehouse=warehouse,
                role=role
            )
        return self._connection

    def execute_query(self, query):
        """
        Execute a SQL query and return the result.
        """
        if not self._connection:
            raise ConnectionError("Snowflake connection is not established.")
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def close_connection(self):
        """
        Close the Snowflake connection.
        """
        if self._connection:
            self._connection.close()
            self._connection = None

