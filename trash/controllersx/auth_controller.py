from flask import Blueprint, request, jsonify
from models import db, User, Merchant  # Assuming you have User and Merchant models
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register_user():
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

@auth_bp.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/auth/merchant/register', methods=['POST'])
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