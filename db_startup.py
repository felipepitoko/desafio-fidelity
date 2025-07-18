import os
import psycopg2
from database import get_db_connection

def setup_database():
    """
    Executes SQL commands from a file to set up the PostgreSQL database.
    """
    conn = None
    try:
        conn = get_db_connection()
        # Use a 'with' statement for the cursor to ensure it's always closed
        with conn.cursor() as cursor:
            sql_file_path = 'create_tables.sql'
            if os.path.exists(sql_file_path):
                print(f"Found '{sql_file_path}'. Executing script...")
                with open(sql_file_path, 'r') as sql_file:
                    sql_script = sql_file.read()
                    # psycopg2 can execute multi-statement strings directly without 'multi=True'
                    cursor.execute(sql_script)
                print("SQL script executed.")
            else:
                print(f"Warning: '{sql_file_path}' not found. Skipping table creation.")

        # Commit the transaction
        conn.commit()
        print("Database setup complete. Transaction committed.")
    except psycopg2.Error as e:
        print(f"Error setting up database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
