import os
import psycopg2

# Replace these values with your actual connection parameters

try:
    # Attempt to connect to CockroachDB
    conn = psycopg2.connect(
        os.environ['DATABASE_URL'])
    print("Connection to CockroachDB successful!")

    # Optionally, you can execute a test query here
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        print("Test query result:", result)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection in any case
    if conn:
        conn.close()


