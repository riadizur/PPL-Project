#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Activate the virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found! Please run install.sh first."
    exit 1
fi

# Set the FLASK_APP environment variable
export FLASK_APP=app.py
export FLASK_DEBUG=1  # Set debug mode
# Check if Flask is installed
if ! command -v flask &> /dev/null; then
    echo "Flask not found! Make sure it's installed in your virtual environment."
    exit 1
fi

# Set the FLASK_ENV environment variable for development (change to 'production' as needed)
export FLASK_ENV=development

# Run the Flask application
echo "Starting Flask application..."
flask run