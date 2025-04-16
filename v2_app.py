from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from v2_api_controllers import router as api_router  # Import the router from v2_api_controllers

# Database URL (you can change this as needed)
DATABASE_URL = "sqlite:///./data/v2_hotel.db"

# FastAPI app setup
app = FastAPI()

# CORS configuration - allows cross-origin requests from all origins
origins = [
    "*",  # Allows all origins, use specific domain names for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router into the main FastAPI application
app.include_router(api_router, prefix="/api/v1", tags=["API"])  # Add prefix and optional tags for organization

# Custom root endpoint to show API structure with methods, description, and parameters
@app.get("/", response_class=JSONResponse)
def read_root():
    return {
        "message": "Welcome to the Hotel Management API",
        "api_documentation": {
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "available_endpoints": {
                "/api/v1/users": {
                    "methods": ["GET", "POST"],
                    "description": "User related operations (create, list users)",
                    "parameters": [
                        {"name": "email", "type": "string", "required": "POST only", "description": "Email of the user."},
                        {"name": "password", "type": "string", "required": "POST only", "description": "Password for the user."},
                        {"name": "role", "type": "string", "required": "POST only", "description": "Role of the user (customer, merchant, admin)."}
                    ]
                },
                "/api/v1/merchants": {
                    "methods": ["GET", "POST"],
                    "description": "Merchant related operations (create, list merchants)",
                    "parameters": [
                        {"name": "user_id", "type": "integer", "required": "POST only", "description": "User ID associated with the merchant."},
                        {"name": "company_name", "type": "string", "required": "POST only", "description": "Company name of the merchant."},
                        {"name": "tax_number", "type": "string", "required": "POST only", "description": "Tax number for the merchant."}
                    ]
                },
                "/api/v1/hotels": {
                    "methods": ["GET", "POST", "PUT", "DELETE"],
                    "description": "Hotel management (CRUD operations)",
                    "parameters": [
                        {"name": "name", "type": "string", "required": "POST, PUT only", "description": "Hotel name."},
                        {"name": "address", "type": "string", "required": "POST, PUT only", "description": "Address of the hotel."},
                        {"name": "city", "type": "string", "required": "POST, PUT only", "description": "City of the hotel."},
                        {"name": "status", "type": "string", "required": "PUT only", "description": "Status of the hotel (active, inactive)."}
                    ]
                },
                "/api/v1/rooms": {
                    "methods": ["GET", "POST", "PUT", "DELETE"],
                    "description": "Room management (CRUD operations)",
                    "parameters": [
                        {"name": "hotel_id", "type": "integer", "required": "POST, PUT only", "description": "ID of the associated hotel."},
                        {"name": "room_number", "type": "string", "required": "POST, PUT only", "description": "Room number."},
                        {"name": "price_per_night", "type": "decimal", "required": "POST, PUT only", "description": "Price per night of the room."}
                    ]
                },
                "/api/v1/bookings": {
                    "methods": ["GET", "POST"],
                    "description": "Booking operations (create, list bookings)",
                    "parameters": [
                        {"name": "user_id", "type": "integer", "required": "POST only", "description": "ID of the user making the booking."},
                        {"name": "room_id", "type": "integer", "required": "POST only", "description": "ID of the room being booked."},
                        {"name": "check_in_date", "type": "datetime", "required": "POST only", "description": "Booking check-in date."},
                        {"name": "check_out_date", "type": "datetime", "required": "POST only", "description": "Booking check-out date."}
                    ]
                },
                "/api/v1/payments": {
                    "methods": ["GET", "POST"],
                    "description": "Payment related operations",
                    "parameters": [
                        {"name": "booking_id", "type": "integer", "required": "POST only", "description": "ID of the booking."},
                        {"name": "amount", "type": "decimal", "required": "POST only", "description": "Amount to be paid."},
                        {"name": "payment_method", "type": "string", "required": "POST only", "description": "Payment method (credit_card, bank_transfer, e_wallet)."}
                    ]
                },
                "/api/v1/reviews": {
                    "methods": ["GET", "POST"],
                    "description": "Review related operations",
                    "parameters": [
                        {"name": "booking_id", "type": "integer", "required": "POST only", "description": "ID of the booking."},
                        {"name": "rating", "type": "integer", "required": "POST only", "description": "Rating of the room (1-5)."},
                        {"name": "comment", "type": "string", "required": "POST only", "description": "Review comment."}
                    ]
                }
            }
        },
        "note": "You can also access detailed API documentation at /docs or /redoc"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}