# app/routes.py
from flask import render_template, request, redirect, url_for, flash, session
from functools import wraps
from .models import Room, Guest, Booking, User

def init_app(app):
    # Authentication Decorator
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    # Authentication Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.authenticate(username, password)
            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                session['role'] = user[4]
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return redirect(url_for('register'))
            
            user_id = User.create_user(username, email, password)
            if user_id:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Username or email already exists', 'error')
        
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out', 'success')
        return redirect(url_for('login'))

    # Main Routes
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    # Room Routes
    @app.route('/rooms')
    @login_required
    def list_rooms():
        rooms = Room.get_all_rooms()
        return render_template('rooms.html', rooms=rooms)

    @app.route('/rooms/add', methods=['GET', 'POST'])
    @login_required
    def add_room():
        if request.method == 'POST':
            room_number = request.form['room_number']
            room_type = request.form['room_type']
            capacity = request.form['capacity']
            price = request.form['price']
            
            Room.create_room(room_number, room_type, capacity, price)
            return redirect(url_for('list_rooms'))
        return render_template('rooms.html', action='add')

    @app.route('/rooms/edit/<int:room_id>', methods=['GET', 'POST'])
    @login_required
    def edit_room(room_id):
        if request.method == 'POST':
            room_number = request.form['room_number']
            room_type = request.form['room_type']
            capacity = request.form['capacity']
            price = request.form['price']
            
            Room.update_room(room_id, room_number, room_type, capacity, price)
            return redirect(url_for('list_rooms'))
        
        room = Room.get_room_by_id(room_id)
        return render_template('rooms.html', action='edit', room=room)

    @app.route('/rooms/delete/<int:room_id>')
    @login_required
    def delete_room(room_id):
        Room.delete_room(room_id)
        return redirect(url_for('list_rooms'))

    # Guest Routes
    @app.route('/guests')
    @login_required
    def list_guests():
        guests = Guest.get_all_guests()
        return render_template('guests.html', guests=guests)

    @app.route('/guests/add', methods=['GET', 'POST'])
    @login_required
    def add_guest():
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            
            Guest.create_guest(first_name, last_name, email, phone, address)
            return redirect(url_for('list_guests'))
        return render_template('guests.html', action='add')

    @app.route('/guests/edit/<int:guest_id>', methods=['GET', 'POST'])
    @login_required
    def edit_guest(guest_id):
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']
            
            Guest.update_guest(guest_id, first_name, last_name, email, phone, address)
            return redirect(url_for('list_guests'))
        
        guest = Guest.get_guest_by_id(guest_id)
        return render_template('guests.html', action='edit', guest=guest, guest_id=guest_id)

    @app.route('/guests/delete/<int:guest_id>')
    @login_required
    def delete_guest(guest_id):
        Guest.delete_guest(guest_id)
        return redirect(url_for('list_guests'))

    # Booking Routes
    @app.route('/bookings')
    @login_required
    def bookings():
        try:
            all_bookings = Booking.get_all_bookings()
            print(f"Retrieved bookings in route: {all_bookings}")
            return render_template('bookings.html', bookings=all_bookings)
        except Exception as e:
            print(f"Error in bookings route: {e}")
            flash('Error loading bookings', 'error')
            return render_template('bookings.html', bookings=[])

    @app.route('/add_booking', methods=['GET', 'POST'])
    @login_required
    def add_booking():
        if request.method == 'POST':
            try:
                guest_id = request.form['guest_id']
                room_id = request.form['room_id']
                check_in_date = request.form['check_in_date']
                check_out_date = request.form['check_out_date']
                total_price = request.form['total_price']
            
                print(f"Attempting to create booking with: Guest ID: {guest_id}, Room ID: {room_id}, Check-in: {check_in_date}, Check-out: {check_out_date}, Total Price: {total_price}")  # Debug print
            
                booking_id = Booking.create_booking(guest_id, room_id, check_in_date, check_out_date, total_price)
                if booking_id:
                    print(f"Booking created successfully with ID: {booking_id}")  # Debug print
                    flash('Booking added successfully!', 'success')
                    return redirect(url_for('bookings'))
                else:
                    print("Failed to create booking")  # Debug print
                    flash('Error adding booking', 'error')
            except Exception as e:
                print(f"Error in add_booking: {e}")  # Debug print
                flash('Error adding booking', 'error')
    
        return render_template('bookings.html', action='add')

    @app.route('/bookings/edit/<int:booking_id>', methods=['GET', 'POST'])
    @login_required
    def edit_booking(booking_id):
        booking = Booking.get_booking_by_id(booking_id)
        if request.method == 'POST':
            guest_id = request.form['guest_id']
            room_id = request.form['room_id']
            check_in_date = request.form['check_in_date']
            check_out_date = request.form['check_out_date']
            total_price = request.form['total_price']
        
            if Booking.update_booking(booking_id, guest_id, room_id, check_in_date, check_out_date, total_price):
                flash('Booking updated successfully!', 'success')
                return redirect(url_for('bookings'))
            else:
                flash('Error updating booking. Please try again.', 'error')
    
        return render_template('bookings.html', action='edit', booking=booking)

    @app.route('/bookings/delete/<int:booking_id>')
    @login_required
    def delete_booking(booking_id):
        if Booking.delete_booking(booking_id):
            flash('Booking deleted successfully!', 'success')
        else:
            flash('Error deleting booking. Please try again.', 'error')
        return redirect(url_for('bookings'))

    