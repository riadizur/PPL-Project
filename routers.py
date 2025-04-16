from flask import Blueprint, render_template, request, jsonify
from models import db, User, Merchant, Room, Facility, Booking, Payment
from werkzeug.security import generate_password_hash, check_password_hash

page = Blueprint('page', __name__, )


@page.route('/', methods=['GET'])
def index():
    return render_template('landing_page.html'),200

@page.route('/login', methods=['GET'])
def login():
    return render_template('login.html'),200

@page.route('/register', methods=['GET'])
def register():
    return render_template('register.html'),200

@page.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template('forgot-password.html'),200

@page.route('/hotels', methods=['GET'])
def hotels():
    return render_template('hotel.html'),200