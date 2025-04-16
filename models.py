from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    business_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    suspended = db.Column(db.Boolean, default=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    merchant = db.relationship('Merchant', backref='rooms')
    facilities = db.relationship('Facility', secondary='room_facility')
    bookings = db.relationship('Booking', backref='room', cascade="all, delete-orphan")

class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(255))  # Field for facility icon
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    merchant = db.relationship('Merchant', backref='facilities')

class RoomFacility(db.Model):
    __tablename__ = 'room_facility'
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), primary_key=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    check_in = db.Column(db.String(50), nullable=False)
    check_out = db.Column(db.String(50), nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='booked')
    payment = db.relationship('Payment', backref='booking', uselist=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(120))
    status = db.Column(db.String(50), default='pending')

class MerchantRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    room = db.relationship('Room', backref='merchant_rooms')
    merchant = db.relationship('Merchant', backref='merchant_rooms')

class MerchantFacility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    facility = db.relationship('Facility', backref='merchant_facilities')
    merchant = db.relationship('Merchant', backref='merchant_facilities')

class DoorAccess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    action = db.Column(db.String(50), nullable=False)  # e.g., 'lock', 'unlock'
    access_token = db.Column(db.String(255), nullable=False)

class QRCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    qr_code = db.Column(db.String(255), nullable=False)  # Store the QR code string
    is_valid = db.Column(db.Boolean, default=True)  # To check if QR is valid

class AdminAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    revenue = db.Column(db.Float, nullable=False)
    occupancy_rate = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    merchant = db.relationship('Merchant', backref='analytics')

class MerchantBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    booking = db.relationship('Booking', backref='merchant_bookings')
    merchant = db.relationship('Merchant', backref='merchant_bookings')

class MerchantAnalytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    total_revenue = db.Column(db.Float)
    total_bookings = db.Column(db.Integer)
    occupancy_rate = db.Column(db.Float)
    merchant = db.relationship('Merchant', backref='merchant_analytics')

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    room_name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    company = db.Column(db.String(), nullable=False)
    posted_date = db.Column(db.String(100), nullable=False)
    page_link = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    facility = db.Column(db.String(), nullable=False)
    room_type = db.Column(db.String(), nullable=False)
# Add any other models as necessary