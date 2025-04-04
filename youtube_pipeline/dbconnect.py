import oracledb
import os
from typing import List, Tuple, Dict, Any
from contextlib import contextmanager

# Enable thin mode (no Oracle Client needed)
# oracledb.init_oracle_client()

@contextmanager
def get_connection(
    username: str = None, password: str = None, host: str = None,
    port: int = 1521, service_name: str = None, role: str = None,
    dsn: str = None
):
    """
    Establish a connection to an Oracle database.
    Uses environment variables if parameters are not provided.

    Returns:
        Connection object if successful, else None.
    """
    try:
        username = username or os.getenv("ORACLE_USER")
        password = password or os.getenv("ORACLE_PWD")
        host = host or os.getenv("ORACLE_HOST")
        port = port or int(os.getenv("ORACLE_PORT", 1521))
        service_name = service_name or os.getenv("ORACLE_SERVICE")

        if not any([all([username, password, host, service_name]), 
                       all([username, password, dsn])]):
            raise ValueError("Missing required Oracle DB connection parameters.")

        dsn = dsn or f"{host}:{port}/{service_name}"
        
        try:
            if role == 'SYSDBA':
                conn = oracledb.connect(user=username, password=password, dsn=dsn, mode=oracledb.SYSDBA)
            else:
                conn = oracledb.connect(user=username, password=password, dsn=dsn)
            print("✅ Connected to Oracle Database successfully!")
            yield conn
        except oracledb.DatabaseError as e:
            raise e
        finally:
            conn.close()
    except oracledb.DatabaseError as e:
        print(f"❌ Database connection failed: {e}")
        return None

def execute_query(conn, query: str, params: Tuple = ()):
    """
    Executes a SQL query and returns the results.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except oracledb.DatabaseError as e:
        print(f"❌ Query execution failed: {e}")
        return []

def execute_dml(conn, query: str, params: Tuple = ()):
    """
    Executes INSERT, UPDATE, DELETE and commits.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            print("✅ DML operation successful.")
    except oracledb.DatabaseError as e:
        print(f"❌ DML operation failed: {e}")
        conn.rollback()

def bulk_insert(conn, schema_name: str, table_name: str, columns: List[str], data: List[Tuple], allowed_tables: List[str]):
    """
    Performs efficient batch insert into an Oracle table.
    """
    if schema_name not in ['ETL_DEV', 'STAGE', 'LOG']:
        raise ValueError(f"Table name '{schema_name}.{table_name}' is not allowed.")
    
    try:
        with conn.cursor() as cursor:
            col_str = ", ".join(columns)
            bind_str = ", ".join([f":{i+1}" for i in range(len(columns))])
            sql = f"INSERT INTO {schema_name}.{table_name} ({col_str}) VALUES ({bind_str})"
            cursor.executemany(sql, data)
            conn.commit()
            print(f"✅ {cursor.rowcount} rows inserted successfully into {schema_name}.{table_name}.")
    except oracledb.DatabaseError as e:
        print(f"❌ Bulk insert failed: {e}")
        conn.rollback()

def fetch_data_as_dict(conn, query: str, params: Tuple = ()):
    """
    Fetch query results as a list of dictionaries (column_name: value).
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except oracledb.DatabaseError as e:
        print(f"❌ Fetch failed: {e}")

def execute_sql_file(conn, sql_file_path):
    try:
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
            print(sql_script[:50])
        sql_statements = [stmt.strip() for stmt in sql_script.split('/') if stmt.strip()]
        with conn.cursor() as cur:
            cur.callproc("dbms_output.enable")
            for statement in sql_statements:
                cur.execute(statement)
                print(f"Executed: {statement[:50]}...")
            """Fetch DBMS_OUTPUT lines in chunks."""
            chunk_size = 100
            lines_var = cur.arrayvar(str, chunk_size)  # Array variable for output lines
            num_lines_var = cur.var(int)  # Variable to hold number of lines retrieved
            num_lines_var.setvalue(0, chunk_size)  # Set chunk size
            while True:
                cur.callproc("DBMS_OUTPUT.GET_LINES", (lines_var, num_lines_var))  # Fetch lines
                num_lines = num_lines_var.getvalue()  # Number of lines retrieved
                lines = lines_var.getvalue()[:num_lines]  # Extract valid lines
                for line in lines:
                    print("DBMS_OUTPUT:", line or "")  # Print output
                if num_lines < chunk_size:  # Stop if fewer lines fetched than chunk size
                    break
        conn.commit()
    except Exception as e:
        conn.rollback()

def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
        print("🔌 Connection closed.")
        

