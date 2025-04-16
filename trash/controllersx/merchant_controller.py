from flask import Blueprint, request, jsonify
from models import db, MerchantRoom, MerchantFacility

merchant_bp = Blueprint('merchant', __name__)

@merchant_bp.route('/merchant/rooms', methods=['GET'])
def get_merchant_rooms():
    # Retrieve merchant's rooms
    rooms = MerchantRoom.query.filter_by(merchant_id=request.user.id).all()
    return jsonify([room.to_dict() for room in rooms])

@merchant_bp.route('/merchant/rooms', methods=['POST'])
def add_merchant_room():
    data = request.get_json()
    new_room = MerchantRoom(**data)
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'Room added successfully'}), 201

# Add other merchant-related endpoints similarly