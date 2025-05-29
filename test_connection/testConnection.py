from session import get_snowpark_session  # Adjust import if needed

def test_snowflake_connection():
    session = get_snowpark_session()
    
    # Run a simple query to check connection
    result = session.sql("SELECT CURRENT_VERSION()").collect()
    
    print("Snowflake version:", result[0][0])

if __name__ == "__main__":
    test_snowflake_connection()
