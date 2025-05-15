from database.db_connection import create_connection

def check_database_connection():
    """
    Check if the database connection is successful.
    """
    conn = create_connection("database/system.db")
    if conn:
        print("Database connection is active.")
        conn.close()
    else:
        print("Failed to connect to the database.")

def handle_database_error(error):
    """
    Handle database-related errors.
    :param error: Error object
    """
    print(f"Database error occurred: {error}")