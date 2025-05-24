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
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    birthday TEXT,
                    password_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Table 'users' created successfully.")
        except Exception as e:
            print(f"Error creating users table: {e}")
        finally:
            close_connection(conn)

def create_attendance_table():
    """
    Create an attendance table in the database if it doesn't exist.
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    confidence REAL,
                    datetime TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Table 'attendance' created successfully.")
        except Exception as e:
            print(f"Error creating attendance table: {e}")
        finally:
            close_connection(conn)

def insert_user(name, email, phone, birthday, password_hash):
    """
    Insert a new user into the users table.
    :param name: User's name
    :param email: User's email
    :param phone: User's phone
    :param birthday: User's birthday
    :param password_hash: User's password hash
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, phone, birthday, password_hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, birthday, password_hash))
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
    # Đảm bảo bảng users tồn tại trước khi truy vấn
    create_users_table()
    import sqlite3
    conn = sqlite3.connect('database/system.db')
    cursor = conn.cursor()
    # Trả về đầy đủ các trường
    cursor.execute("SELECT id, name, email, phone, birthday, password_hash, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def insert_attendance_from_csv(csv_path):
    """
    Insert data from a CSV file into the attendance table.
    :param csv_path: Path to the CSV file
    """
    # Đảm bảo bảng attendance tồn tại trước khi insert
    create_attendance_table()
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                # Bỏ qua dòng tổng kết nếu có
                if row.get("Name") and row.get("Name") != "Summary":
                    cursor.execute('''
                        INSERT INTO attendance (name, confidence, datetime)
                        VALUES (?, ?, ?)
                    ''', (row.get("Name"), row.get("Confidence"), row.get("Datetime")))
            conn.commit()
            print(f"Attendance data from {csv_path} inserted into 'attendance' table successfully.")
        except Exception as e:
            print(f"Error inserting attendance from CSV: {e}")
        finally:
            close_connection(conn)

def update_user(user_id, name, email, phone, birthday):
    """
    Update user info (except password) by id.
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET name=?, email=?, phone=?, birthday=? WHERE id=?
            ''', (name, email, phone, birthday, user_id))
            conn.commit()
        except Exception as e:
            print(f"Error updating user: {e}")
        finally:
            close_connection(conn)

def delete_user(user_id):
    """
    Delete user by id.
    """
    conn = create_connection("database/system.db")
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
            conn.commit()
        except Exception as e:
            print(f"Error deleting user: {e}")
        finally:
            close_connection(conn)