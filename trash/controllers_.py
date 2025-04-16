from flask import Blueprint, jsonify, request
from models import db, User, Merchant, Room, Booking, Payment, Facility, RoomFacility
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Create a blueprint for the API endpoints
api = Blueprint('api', __name__, url_prefix='/api/v1')

# AUTHENTICATION CONTROLLERS

@api.route('/auth/register', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password=hashed_password, name=data['name'], phone=data['phone'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@api.route('/auth/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@api.route('/auth/merchant/register', methods=['POST'])
def register_merchant():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_merchant = Merchant(email=data['email'], password=hashed_password, business_name=data['business_name'],
                            address=data['address'], phone=data['phone'])
    db.session.add(new_merchant)
    db.session.commit()
    return jsonify({"message": "Merchant registered successfully!"})


# CUSTOMER CONTROLLERS

@api.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    room_list = [{"id": room.id, "name": room.name, "type": room.type, "price": room.price} for room in rooms]
    return jsonify(room_list)

@api.route('/rooms/<int:id>', methods=['GET'])
def get_room_details(id):
    room = Room.query.get_or_404(id)
    return jsonify({"id": room.id, "name": room.name, "type": room.type, "price": room.price, "facilities": room.facilities})

@api.route('/rooms/search', methods=['GET'])
def search_rooms():
    keyword = request.args.get('keyword')
    location = request.args.get('location')
    # Additional filters can be implemented based on requirements
    rooms = Room.query.filter(Room.name.contains(keyword)).all()
    room_list = [{"id": room.id, "name": room.name, "type": room.type, "price": room.price} for room in rooms]
    return jsonify(room_list)

@api.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    new_booking = Booking(room_id=data['room_id'], check_in=data['check_in'], check_out=data['check_out'], guest_count=data['guest_count'])
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"message": "Booking created successfully!"})

@api.route('/bookings', methods=['GET'])
def get_booking_history():
    bookings = Booking.query.all()  # Modify to filter by user
    booking_list = [{"id": booking.id, "room_id": booking.room_id, "check_in": booking.check_in, "check_out": booking.check_out} for booking in bookings]
    return jsonify(booking_list)

@api.route('/bookings/<int:id>', methods=['GET'])
def get_booking_details(id):
    booking = Booking.query.get_or_404(id)
    return jsonify({"id": booking.id, "room_id": booking.room_id, "check_in": booking.check_in, "check_out": booking.check_out})

@api.route('/bookings/<int:id>/cancel', methods=['PUT'])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    booking.status = 'cancelled'
    db.session.commit()
    return jsonify({"message": "Booking cancelled successfully!"})


# PAYMENTS CONTROLLERS

@api.route('/payments/initialize', methods=['POST'])
def initialize_payment():
    data = request.json
    new_payment = Payment(booking_id=data['booking_id'], payment_method=data['payment_method'])
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({"message": "Payment initialized successfully!"})

@api.route('/payments/confirm', methods=['POST'])
def confirm_payment():
    data = request.json
    payment = Payment.query.get_or_404(data['payment_id'])
    payment.transaction_id = data['transaction_id']
    payment.status = 'confirmed'
    db.session.commit()
    return jsonify({"message": "Payment confirmed successfully!"})

@api.route('/payments/<int:id>/status', methods=['GET'])
def check_payment_status(id):
    payment = Payment.query.get_or_404(id)
    return jsonify({"status": payment.status})

# Add other controllers for Merchant and Admin as needed