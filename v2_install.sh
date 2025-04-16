#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create and activate virtual environment
print_message "Creating Python virtual environment..."
if [ -d "venv2" ]; then
    print_message "Virtual environment already exists. Removing old environment..."
    rm -rf venv2
fi

python3 -m venv venv2
if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment."
    exit 1
fi
print_success "Virtual environment created successfully."

# Activate virtual environment
print_message "Activating virtual environment..."
source venv2/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip
print_message "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r v2_requirements.txt
pip install --upgrade sqlalchemy

# Verify installations
print_message "Verifying installations..."
python -c "import fastapi" || {
    print_error "FastAPI not properly installed. Attempting reinstall..."
    pip uninstall fastapi -y
    pip install fastapi --no-cache-dir
    python -c "import fastapi" || {
        print_error "FastAPI installation failed. Please try manually with: pip install fastapi"
        exit 1
    }
}

python -c "import uvicorn" || {
    print_error "Uvicorn not properly installed. Attempting reinstall..."
    pip uninstall uvicorn -y
    pip install "uvicorn[standard]" --no-cache-dir
    python -c "import uvicorn" || {
        print_error "Uvicorn installation failed. Please try manually with: pip install uvicorn[standard]"
        exit 1
    }
}
print_success "Requirements installed successfully."
# Setup environment variables (optional, create .env if not exists)
if [ ! -f ".env" ]; then
    echo "Creating .env file for environment variables..."
    touch .env
    echo "DATABASE_URL=sqlite:///./data/v2_hotel.db" >> .env
    echo "SECRET_KEY=ppl-project" >> .env
    echo "JWT_ALGORITHM=HS256" >> .env
    echo "JWT_EXPIRATION_DELTA=3600" >> .env
    echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env
    print_success ".env file created successfully."
fi

# Create necessary directories
print_message "Creating project directories..."
mkdir -p logs
mkdir -p data

print_success "Installation completed successfully!"
print_message "To activate the virtual environment, run: source venv2/bin/activate"
print_message "To start the application, run: python -m uvicorn app:app --reload"

# Deactivate virtual environment
deactivate