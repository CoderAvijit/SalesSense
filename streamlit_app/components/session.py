from snowflake.snowpark import Session
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_snowpark_session():
    connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA")
    }

    # Optional: Debug print to verify all values are set
    for key, value in connection_parameters.items():
        if not value:
            raise ValueError(f"Missing value for {key}. Please check your .env file or environment variables.")

    # Create and return the session
    return Session.builder.configs(connection_parameters).create()
