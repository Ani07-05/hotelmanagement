from app.database import DatabaseManager
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    @staticmethod
    def create_user(username, email, password, role='guest'):
        db = DatabaseManager()
        hashed_password = generate_password_hash(password)
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, email, password, role)
                    VALUES (?, ?, ?, ?)
                ''', (username, email, hashed_password, role))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def authenticate(username, password):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[3], password):
                return user
            return None

    @staticmethod
    def get_user_by_id(user_id):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            return cursor.fetchone()

class Room:
    @staticmethod
    def create_room(room_number, room_type, capacity, price):
        db = DatabaseManager()
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO rooms (room_number, room_type, capacity, price)
                    VALUES (?, ?, ?, ?)
                ''', (room_number, room_type, capacity, price))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_all_rooms():
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rooms')
            return cursor.fetchall()

    @staticmethod
    def get_room_by_id(room_id):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
            return cursor.fetchone()

    @staticmethod
    def update_room(room_id, room_number, room_type, capacity, price):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE rooms 
                SET room_number=?, room_type=?, capacity=?, price=?
                WHERE id=?
            ''', (room_number, room_type, capacity, price, room_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_room(room_id):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM rooms WHERE id=?', (room_id,))
            conn.commit()
            return cursor.rowcount > 0

class Guest:
    @staticmethod
    def create_guest(first_name, last_name, email, phone, address):
        db = DatabaseManager()
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO guests (first_name, last_name, email, phone, address)
                    VALUES (?, ?, ?, ?, ?)
                ''', (first_name, last_name, email, phone, address))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_all_guests():
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM guests')
            return cursor.fetchall()

    @staticmethod
    def get_guest_by_id(guest_id):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM guests WHERE id = ?', (guest_id,))
            return cursor.fetchone()

    @staticmethod
    def update_guest(guest_id, first_name, last_name, email, phone, address):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE guests 
                SET first_name=?, last_name=?, email=?, phone=?, address=?
                WHERE id=?
            ''', (first_name, last_name, email, phone, address, guest_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_guest(guest_id):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM guests WHERE id=?', (guest_id,))
            conn.commit()
            return cursor.rowcount > 0

class Booking:
    # @staticmethod
    # def create_booking(guest_id, room_id, check_in_date, check_out_date, total_price):
    #     db = DatabaseManager()
    #     try:
    #         with db.get_connection() as conn:
    #             cursor = conn.cursor()
    #             cursor.execute('''
    #                 INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date, total_price)
    #                 VALUES (?, ?, ?, ?, ?)
    #             ''', (guest_id, room_id, check_in_date, check_out_date, total_price))
    #             conn.commit()
    #             return cursor.lastrowid
    #     except Exception as e:
    #         # Log the error or print it for debugging
    #         print(f"Error creating booking: {e}")
    #         conn.rollback()
    #         return None
        
    @staticmethod
    @staticmethod
    def get_all_bookings():
        db = DatabaseManager()
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                
                # First, let's check if the bookings table exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings';")
                if not cursor.fetchone():
                    print("The 'bookings' table does not exist in the database.")
                    return []

                # Now, let's check if there are any records in the bookings table
                cursor.execute("SELECT COUNT(*) FROM bookings;")
                count = cursor.fetchone()[0]
                print(f"Number of records in the bookings table: {count}")

                # If there are records, let's fetch them
                if count > 0:
                    cursor.execute('''
                        SELECT 
                            b.id,
                            g.first_name || ' ' || g.last_name as guest_name,
                            r.room_number,
                            b.check_in_date,
                            b.check_out_date,
                            b.total_price,
                            b.status
                        FROM bookings b
                        JOIN guests g ON b.guest_id = g.id
                        JOIN rooms r ON b.room_id = r.id
                        ORDER BY b.check_in_date DESC
                    ''')
                    bookings = cursor.fetchall()
                    print(f"Retrieved {len(bookings)} bookings")
                    for booking in bookings:
                        print(f"Booking: {dict(booking)}")
                    return [dict(row) for row in bookings]
                else:
                    print("No bookings found in the database.")
                    return []
        except Exception as e:
            print(f"Error fetching bookings: {e}")
            return []
    @staticmethod
    def create_booking(guest_id, room_id, check_in_date, check_out_date, total_price):
        db = DatabaseManager()
        try:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date, total_price, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (guest_id, room_id, check_in_date, check_out_date, total_price, 'Confirmed'))
                conn.commit()
                print(f"Booking created with ID: {cursor.lastrowid}")  # Debug print
                return cursor.lastrowid
        except Exception as e:
            print(f"Error creating booking: {e}")
            return None

    @staticmethod
    def get_booking_by_id(booking_id):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM bookings WHERE id = ?
            ''', (booking_id,))
            return cursor.fetchone()

    @staticmethod
    def update_booking_status(booking_id, status):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bookings 
                SET status = ?
                WHERE id = ?
            ''', (status, booking_id))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete_booking(booking_id):
        db = DatabaseManager()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bookings WHERE id=?', (booking_id,))
            conn.commit()
            return cursor.rowcount > 0