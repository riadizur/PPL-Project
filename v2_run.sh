#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print colored message
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to cleanup on script exit
cleanup() {
    print_message "Shutting down application..."
    if [ -f "app.pid" ]; then
        pid=$(cat app.pid)
        kill $pid 2>/dev/null
        rm app.pid
    fi
    deactivate 2>/dev/null
    print_success "Shutdown complete"
    exit 0
}

# Trap SIGINT and SIGTERM signals
trap cleanup SIGINT SIGTERM

# Check if virtual environment exists
if [ ! -d "venv2" ]; then
    print_error "Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Using default settings."
    export API_HOST="0.0.0.0"
    export API_PORT="443"
    export DEBUG_MODE="True"
else
    print_message "Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
fi

# Activate virtual environment
print_message "Activating virtual environment..."
source venv2/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment."
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Get current timestamp for log file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="logs/app_${TIMESTAMP}.log"

print_message "Starting application..."
print_message "API will be available at http://${API_HOST}:${API_PORT}"
print_message "API documentation will be available at http://${API_HOST}:${API_PORT}/docs"
print_message "Logs will be written to ${LOG_FILE}"

# Start the application
if [ "$DEBUG_MODE" = "True" ]; then
    print_warning "Running in DEBUG mode with auto-reload enabled"
    python -m uvicorn v2_app:app \
        --host ${API_HOST:-0.0.0.0} \
        --port ${API_PORT:-443} \
        --reload \
        --log-level debug \
        2>&1 | tee -a "${LOG_FILE}" &
else
    print_message "Running in PRODUCTION mode"
    python -m uvicorn v2_app:app \
        --host ${API_HOST:-0.0.0.0} \
        --port ${API_PORT:-443} \
        --workers 4 \
        --log-level info \
        2>&1 | tee -a "${LOG_FILE}" &
fi

# Save PID
echo $! > app.pid

print_success "Application started successfully!"
print_message "Press Ctrl+C to stop the application"

# Wait for the application to exit
wait $!

# Cleanup on exit
cleanup