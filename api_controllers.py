from flask import Blueprint, request, jsonify
from models import db, User, Merchant, Room, Facility, Booking, Payment, Hotel
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__, url_prefix='/api/v1')

# Authentication Endpoints
@api.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(
        email=data['email'],
        password=generate_password_hash(data['password']),
        name=data['name'],
        phone=data['phone']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful','name':user.name}), 200
    return jsonify({'message': 'Invalid Email or Password'}), 401

@api.route('/auth/merchant/register', methods=['POST'])
def register_merchant():
    data = request.get_json()
    new_merchant = Merchant(
        email=data['email'],
        password=generate_password_hash(data['password']),
        business_name=data['business_name'],
        address=data['address'],
        phone=data['phone']
    )
    db.session.add(new_merchant)
    db.session.commit()
    return jsonify({'message': 'Merchant registered successfully'}), 201

@api.route('/hotels', methods=['GET'])
def get_hotels():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=5, type=int)
    search_term = request.args.get('search', default='', type=str).lower()
    hotel_type = request.args.get('type', default='all', type=str)
    qualification = request.args.get('qualification', default='all', type=str)

    # Query the Job table
    query = Hotel.query

    # Filter based on search term if provided
    if search_term:
        query = query.filter(Hotel.name.ilike(f'%{search_term}%'))

    # Filter based on job type if specified
    if hotel_type != 'all':
        query = query.filter(Hotel.type == hotel_type)  # Ensure you have a 'type' field in your Job model

    # Filter based on qualification if specified
    if qualification != 'all':
        query = query.filter(Hotel.qualification == qualification)  # Ensure you have a 'qualification' field in your Job model

    # Apply offset and limit for pagination
    hotels = query.offset(offset).limit(limit).all()
    
    # Format the job listings into a list of dictionaries
    hotel_listings = [{
        'id': hotel.id,
        'name': hotel.name,
        'room_name': hotel.room_name,
        'image': hotel.image,
        'qualification': hotel.qualification,
        'type': hotel.type,
        'company': hotel.company,
        'posted_date': hotel.posted_date,
        'page_link': hotel.page_link,
        'description': hotel.description,
        'location' : hotel.location,
        'price' : hotel.price,
        'facility': hotel.facility,
        'room_type': hotel.room_type
    } for hotel in hotels]

    return jsonify(hotel_listings),200

@api.route('/hotels/<int:id>', methods=['GET'])

def get_hotel(id):
    hotels = Hotel.query.get_or_404(id)
    # Format the job listings into a list of dictionaries
    hotel_listings = [{
        'id': hotel.id,
        'name': hotel.name,
        'room_name': hotel.room_name,
        'image': hotel.image,
        'qualification': hotel.qualification,
        'type': hotel.type,
        'company': hotel.company,
        'posted_date': hotel.posted_date,
        'page_link': hotel.page_link,
        'description': hotel.description,
        'price' : hotel.price,
        'facility': hotel.facility,
        'room_type': hotel.room_type
    } for hotel in hotels]

    return jsonify(hotel_listings),200

# Room Endpoints
@api.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{'id': room.id, 'name': room.name, 'type': room.type, 'price': room.price} for room in rooms]), 200

@api.route('/rooms/<int:id>', methods=['GET'])
def get_room(id):
    room = Room.query.get_or_404(id)
    return jsonify({'id': room.id, 'name': room.name, 'type': room.type, 'price': room.price}), 200

@api.route('/rooms/search', methods=['GET'])
def search_rooms():
    keyword = request.args.get('keyword', '')
    # Implement search logic based on keyword, location, and date range
    return jsonify({'message': 'Search functionality not yet implemented'}), 501

# Booking Endpoints
@api.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    new_booking = Booking(
        room_id=data['room_id'],
        check_in=data['check_in'],
        check_out=data['check_out'],
        guest_count=data['guest_count']
    )
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking created successfully', 'booking_id': new_booking.id}), 201

@api.route('/bookings', methods=['GET'])
def get_user_bookings():
    # Placeholder for user authentication and fetching bookings
    return jsonify({'message': 'User booking history not yet implemented'}), 501

@api.route('/bookings/<int:id>', methods=['GET'])
def get_booking(id):
    booking = Booking.query.get_or_404(id)
    return jsonify({'id': booking.id, 'room_id': booking.room_id, 'check_in': booking.check_in, 'check_out': booking.check_out, 'guest_count': booking.guest_count}), 200

@api.route('/bookings/<int:id>/cancel', methods=['PUT'])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking cancelled successfully'}), 200

# Payment Endpoints
@api.route('/payments/initialize', methods=['POST'])
def initialize_payment():
    data = request.get_json()
    new_payment = Payment(
        booking_id=data['booking_id'],
        payment_method=data['payment_method'],
        status='pending'
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment initialized successfully', 'payment_id': new_payment.id}), 201

@api.route('/payments/confirm', methods=['POST'])
def confirm_payment():
    data = request.get_json()
    payment = Payment.query.get_or_404(data['payment_id'])
    payment.transaction_id = data['transaction_id']
    payment.status = 'confirmed'
    db.session.commit()
    return jsonify({'message': 'Payment confirmed successfully'}), 200

@api.route('/payments/<int:id>/status', methods=['GET'])
def check_payment_status(id):
    payment = Payment.query.get_or_404(id)
    return jsonify({'id': payment.id, 'status': payment.status}), 200

# Merchant Endpoints
@api.route('/merchant/rooms', methods=['GET'])
def get_merchant_rooms():
    # Placeholder for fetching merchant's rooms
    return jsonify({'message': 'Fetching merchant rooms not yet implemented'}), 501

@api.route('/merchant/rooms', methods=['POST'])
def add_merchant_room():
    data = request.get_json()
    new_room = Room(
        name=data['name'],
        type=data['type'],
        price=data['price'],
        merchant_id=data['merchant_id']  # Assuming merchant_id is provided
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room added successfully', 'room_id': new_room.id}), 201

@api.route('/merchant/rooms/<int:id>', methods=['PUT'])
def update_merchant_room(id):
    data = request.get_json()
    room = Room.query.get_or_404(id)
    room.name = data['name']
    room.type = data['type']
    room.price = data['price']
    db.session.commit()
    return jsonify({'message': 'Room updated successfully'}), 200

@api.route('/merchant/rooms/<int:id>', methods=['DELETE'])
def delete_merchant_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'}), 200

@api.route('/merchant/facilities', methods=['GET'])
def get_merchant_facilities():
    # Placeholder for fetching merchant's facilities
    return jsonify({'message': 'Fetching merchant facilities not yet implemented'}), 501

@api.route('/merchant/facilities', methods=['POST'])
def add_merchant_facility():
    data = request.get_json()
    new_facility = Facility(
        name=data['name'],
        description=data['description'],
        icon=data['icon'],
        merchant_id=data['merchant_id']  # Assuming merchant_id is provided
    )
    db.session.add(new_facility)
    db.session.commit()
    return jsonify({'message': 'Facility added successfully', 'facility_id': new_facility.id}), 201

@api.route('/merchant/facilities/<int:id>', methods=['PUT'])
def update_merchant_facility(id):
    data = request.get_json()
    facility = Facility.query.get_or_404(id)
    facility.name = data['name']
    facility.description = data['description']
    facility.icon = data['icon']
    db.session.commit()
    return jsonify({'message': 'Facility updated successfully'}), 200

@api.route('/merchant/facilities/<int:id>', methods=['DELETE'])
def delete_merchant_facility(id):
    facility = Facility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return jsonify({'message': 'Facility deleted successfully'}), 200

@api.route('/merchant/bookings', methods=['GET'])
def get_merchant_bookings():
    # Placeholder for fetching merchant's bookings
    return jsonify({'message': 'Fetching merchant bookings not yet implemented'}), 501

# Admin Endpoints
@api.route('/admin/merchants', methods=['GET'])
def get_all_merchants():
    merchants = Merchant.query.all()
    return jsonify([{'id': m.id, 'business_name': m.business_name, 'verified': m.verified} for m in merchants]), 200

@api.route('/admin/merchants/<int:id>/verify', methods=['PUT'])
def verify_merchant(id):
    merchant = Merchant.query.get_or_404(id)
    merchant.verified = True
    db.session.commit()
    return jsonify({'message': 'Merchant verified successfully'}), 200

@api.route('/admin/analytics', methods=['GET'])
def get_analytics():
    # Placeholder for fetching overall analytics data
    return jsonify({'message': 'Fetching analytics not yet implemented'}), 501
    