from database.db_connection import create_connection, close_connection
import pandas as pd

def create_table():
    """
    Create a table in the database if it doesn't exist.
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Table 'users' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            close_connection(conn)

def create_users_table():
    """
    Create a users table in the database if it doesn't exist.
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Table 'users' created successfully.")
        except Exception as e:
            print(f"Error creating users table: {e}")
        finally:
            close_connection(conn)

def create_statistics_table():
    """
    Create a statistics table in the database if it doesn't exist.
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    confidence REAL,
                    total_faces INTEGER,
                    recognized_faces INTEGER,
                    recognition_rate REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Table 'statistics' created successfully.")
        except Exception as e:
            print(f"Error creating statistics table: {e}")
        finally:
            close_connection(conn)

def insert_user(name, email):
    """
    Insert a new user into the users table.
    :param name: User's name
    :param email: User's email
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email) VALUES (?, ?)
            ''', (name, email))
            conn.commit()
            print("User inserted successfully.")
        except Exception as e:
            print(f"Error inserting user: {e}")
        finally:
            close_connection(conn)

def fetch_users():
    """
    Fetch all users from the users table.
    :return: List of users
    """
    import sqlite3
    conn = sqlite3.connect('system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def insert_statistics_from_csv(csv_path):
    """
    Insert data from a CSV file into the statistics table.
    :param csv_path: Path to the CSV file
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            df = pd.read_csv(csv_path)

            for _, row in df.iterrows():
                cursor.execute('''
                    INSERT INTO statistics (name, confidence, total_faces, recognized_faces, recognition_rate)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row.get("Name"), row.get("Confidence"), row.get("Total Faces"), 
                      row.get("Recognized Faces"), row.get("Recognition Rate (%)")))

            conn.commit()
            print(f"Data from {csv_path} inserted into 'statistics' table successfully.")
        except Exception as e:
            print(f"Error inserting statistics from CSV: {e}")
        finally:
            close_connection(conn)  