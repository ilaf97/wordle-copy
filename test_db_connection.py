import psycopg2

# Replace these values with your actual connection parameters

try:
    # Attempt to connect to CockroachDB
    conn = psycopg2.connect(
        "postgresql://isaac.frewin:VYf13U7sFRN9nVIncfh9jA@wordle-copy-3792.6zw.aws-eu-west-1.cockroachlabs.cloud:26257/word-game?sslmode=verify-full")
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


