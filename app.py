from datetime import datetime
from flask import Flask
from models import db
from api_controllers import api
from routers import page
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instances/hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register the API blueprint
app.register_blueprint(api)
app.register_blueprint(page)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()  # Create database tables
    app.run(debug=True)