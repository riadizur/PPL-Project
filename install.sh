#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.8 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
if [ -f requirements.txt ]; then
    echo "Installing required packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found! Please create it with the necessary packages."
    exit 1
fi

# Initialize the database
# echo "Initializing database..."
# python << END
# from app import db, app
# with app.app_context():
#     db.create_all()
# END
# Initialize the database (uncomment the following line if using Flask-Migrate)
# echo "Initializing the database..."
# flask db upgrade

# Any other setup commands can go here

echo "Setup completed successfully!"