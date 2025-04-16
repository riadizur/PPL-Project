from flask import Blueprint, request, jsonify
from models import db, Room, Booking

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/rooms', methods=['GET'])
def get_rooms():
    # Query parameters can be used here for filtering
    # Example: check_in, check_out, price_min, price_max
    rooms = Room.query.all()  # Replace with your filtering logic
    return jsonify([room.to_dict() for room in rooms])

@customer_bp.route('/rooms/<int:id>', methods=['GET'])
def get_room_details(id):
    room = Room.query.get_or_404(id)
    return jsonify(room.to_dict())

@customer_bp.route('/bookings', methods=['POST'])
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
    return jsonify({'message': 'Booking created successfully'}), 201

@customer_bp.route('/bookings/<int:id>', methods=['GET'])
def get_booking_details(id):
    booking = Booking.query.get_or_404(id)
    return jsonify(booking.to_dict())

@customer_bp.route('/bookings/<int:id>/cancel', methods=['PUT'])
def cancel_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking canceled successfully'}), 200

# Add more customer endpoints as needed