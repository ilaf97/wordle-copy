import sqlite3
import os


# Function to test the connection to a database
def test_db_connection(db_url, db_name):
    try:
        # Extract the database path from the URL format
        db_path = db_url.split('///')[1]
        # Establish connection to the SQLite database
        conn = sqlite3.connect(db_path)
        print(f"Connection to {db_name} successful")
        # Optionally, execute a simple query to ensure the database is responsive
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version();")
        print(f"SQLite version for {db_name}:", cursor.fetchone())
        # Close the connection
        conn.close()
    except sqlite3.Error as error:
        print(f"Error while connecting to {db_name}:", error)

# Test connection for main database
test_db_connection(os.getenv('DATABASE_URL'), "main database")

# Test connection for test database
test_db_connection(os.getenv('TEST_DATABASE_URL'), "test database")
