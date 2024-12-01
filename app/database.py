# app/database.py
import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='database/hotel.db'):
        self.db_path = db_path
        self.ensure_database()

    def ensure_database(self):
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Connect to database and create tables if not exist
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'guest'
                )
            ''')
            
            # Rooms Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_number TEXT UNIQUE NOT NULL,
                    room_type TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    status TEXT DEFAULT 'Available'
                )
            ''')
            
            # Guests Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS guests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    address TEXT
                )
            ''')
            
            # Bookings Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guest_id INTEGER,
                    room_id INTEGER,
                    check_in_date TEXT NOT NULL,
                    check_out_date TEXT NOT NULL,
                    total_price REAL NOT NULL,
                    status TEXT DEFAULT 'Confirmed',
                    FOREIGN KEY (guest_id) REFERENCES guests(id),
                    FOREIGN KEY (room_id) REFERENCES rooms(id)
                )
            ''')
            
            conn.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def close_connection(self, connection):
        connection.close()