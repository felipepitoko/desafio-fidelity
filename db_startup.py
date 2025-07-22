import os
import psycopg2
from database import get_db_connection

def execute_sql_from_file(cursor, file_path):
    """
    Reads and executes an SQL script from a given file path.
    Raises an exception if the execution fails.
    """
    if not os.path.exists(file_path):
        print(f"Warning: '{file_path}' not found. Skipping.")
        return

    print(f"Executing script from '{file_path}'...")
    try:
        # Specify UTF-8 encoding for better compatibility
        with open(file_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
            if sql_script.strip():
                cursor.execute(sql_script)
                print(f"Successfully executed '{file_path}'.")
            else:
                print(f"Warning: '{file_path}' is empty. Skipping execution.")
    except (IOError, psycopg2.Error) as e:
        # Re-raise the exception to be caught by the main try-except block
        # which will trigger a transaction rollback.
        print(f"Error during execution of {file_path}: {e}")
        raise


def setup_database():
    """
    Executes SQL commands to create tables and populate them with fake data.
    The entire operation is a single transaction. If any part fails,
    all changes are rolled back.
    """
    conn = None
    try:
        conn = get_db_connection()
        # Use a 'with' statement for the cursor to ensure it's always closed
        with conn.cursor() as cursor:
            print("--- Starting Database Setup ---")

            # 1. Create tables
            execute_sql_from_file(cursor, 'create_tables.sql')

            # 2. Insert fake data
            execute_sql_from_file(cursor, 'fake_data.sql')

        # Commit the transaction
        conn.commit()
        print("--- Database setup complete. Transaction committed. ---")
    except (psycopg2.Error, Exception) as e:
        print("\n--- Database Setup Failed ---")
        print(f"An error occurred: {e}")
        if conn:
            print("Rolling back all changes.")
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    setup_database()
