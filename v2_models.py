from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    phone = Column(Text)
    role = Column(Text, nullable=False)
    is_verified = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # __table_args__ = (CheckConstraint(role.in_(['customer', 'merchant', 'admin'])),)

class Merchant(Base):
    __tablename__ = 'merchants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_name = Column(Text, nullable=False)
    business_license = Column(Text)
    tax_number = Column(Text)
    address = Column(Text)
    phone = Column(Text)
    is_verified = Column(Integer, default=0)
    status = Column(Text, default='inactive')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", backref="merchants")
    # __table_args__ = (CheckConstraint(status.in_(['active', 'suspended', 'inactive'])),)

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    name = Column(Text, nullable=False)
    description = Column(Text)
    address = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    country = Column(Text, nullable=False)
    postal_code = Column(Text)
    phone = Column(Text)
    email = Column(Text)
    rating = Column(Integer)
    type = Column(Text)
    check_in_time = Column(Text)
    check_out_time = Column(Text)
    status = Column(Text, default='active')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    merchant = relationship("Merchant", backref="hotels")
    # __table_args__ = (CheckConstraint(status.in_(['active', 'inactive'])),)

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    name = Column(Text, nullable=False)
    room_number = Column(Text, nullable=False)
    floor_number = Column(Text)
    description = Column(Text)
    type = Column(Text)
    qualification = Column(Text)
    capacity = Column(Integer, nullable=False)
    bed_count = Column(Integer)
    price_per_night = Column(DECIMAL, nullable=False)
    status = Column(Text, default='available')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    hotel = relationship("Hotel", backref="rooms")
    # __table_args__ = (CheckConstraint(status.in_(['available', 'occupied', 'maintenance'])),)

class Facility(Base):
    __tablename__ = 'facilities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    icon = Column(Text)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class RoomFacility(Base):
    __tablename__ = 'room_facilities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    facility_id = Column(Integer, ForeignKey('facilities.id'))
    created_at = Column(DateTime, default=func.now())

    room = relationship("Room", backref="room_facilities")
    facility = relationship("Facility", backref="room_facilities")
    # __table_args__ = (CheckConstraint(room_id.isnot(None), facility_id.isnot(None)),)

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    imageable_type = Column(Text, nullable=False)
    imageable_id = Column(Integer, nullable=False)
    url = Column(Text, nullable=False)
    is_primary = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # __table_args__ = (CheckConstraint(imageable_type.in_(['hotel', 'room'])),)

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    guest_count = Column(Integer, nullable=False)
    total_price = Column(DECIMAL, nullable=False)
    special_requests = Column(Text)
    qr_code = Column(Text, unique=True)
    status = Column(Text, default='pending')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", backref="bookings")
    room = relationship("Room", backref="bookings")
    # __table_args__ = (CheckConstraint(status.in_(['pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled'])),)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    amount = Column(DECIMAL, nullable=False)
    payment_method = Column(Text, nullable=False)
    transaction_id = Column(Text, unique=True)
    status = Column(Text, default='pending')
    paid_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    booking = relationship("Booking", backref="payments")
    # __table_args__ = (CheckConstraint(payment_method.in_(['credit_card', 'bank_transfer', 'e_wallet'])),
    #                  CheckConstraint(status.in_(['pending', 'paid', 'failed', 'refunded'])))

class AccessLog(Base):
    __tablename__ = 'access_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    action = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    error_message = Column(Text)
    created_at = Column(DateTime, default=func.now())

    booking = relationship("Booking", backref="access_logs")
    room = relationship("Room", backref="access_logs")
    # __table_args__ = (CheckConstraint(action.in_(['door_open', 'door_close', 'qr_scan'])),
    #                  CheckConstraint(status.in_(['success', 'failed'])))

class HelpDeskTicket(Base):
    __tablename__ = 'help_desk_tickets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(Text, default='low')
    status = Column(Text, default='open')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", backref="help_desk_tickets")
    booking = relationship("Booking", backref="help_desk_tickets")
    # __table_args__ = (CheckConstraint(priority.in_(['low', 'medium', 'high'])),
    #                  CheckConstraint(status.in_(['open', 'in_progress', 'resolved', 'closed'])))

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    booking = relationship("Booking", backref="reviews")
    user = relationship("User", backref="reviews")
    room = relationship("Room", backref="reviews")


# Database setup
DATABASE_URL = "sqlite:///./data/v2_hotel.db"
# Create an engine to connect to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Specific to SQLite

# Create all tables in the database (if not already created)
Base.metadata.create_all(bind=engine)