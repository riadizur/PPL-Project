from pydantic import BaseModel, Field, condecimal
from typing import Optional
from datetime import datetime

# ----------------- User Schema -----------------
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    phone: Optional[str] = None
    role: str = Field(..., regex="^(customer|merchant|admin)$")

# New UserUpdate schema
class UserUpdate(BaseModel):
    email: Optional[str]
    password: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    role: Optional[str]
    is_verified: Optional[int]

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str]
    role: str
    is_verified: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# ----------------- Merchant Schema -----------------
class MerchantCreate(BaseModel):
    user_id: int
    company_name: str
    business_license: Optional[str] = None
    tax_number: Optional[str] = None
    address: Optional[str] = None
    bank_account: Optional[str] = None
    company_owner: Optional[str] = None
    company_description: Optional[str] = None
    company_email:Optional[str] = None
    # password: Optional[str] = None

class MerchantUpdate(BaseModel):
    user_id: Optional[int]
    company_name: Optional[str]
    business_license: Optional[str]
    tax_number: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    is_verified: Optional[int]
    status: Optional[str]

    class Config:
        orm_mode = True

class Merchant(BaseModel):
    id: int
    user_id: int
    company_name: str
    business_license: Optional[str]
    tax_number: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    is_verified: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# ----------------- Hotel Schema -----------------
class HotelCreate(BaseModel):
    merchant_id: int
    name: str
    description: Optional[str]
    address: str
    city: str
    country: str
    postal_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    rating: Optional[float] = None
    type: Optional[str]
    check_in_time: Optional[str]
    check_out_time: Optional[str]

# New HotelUpdate schema
class HotelUpdate(BaseModel):
    merchant_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    rating: Optional[float]
    type: Optional[str]
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True

class Hotel(BaseModel):
    id: int
    merchant_id: int
    name: str
    description: Optional[str]
    address: str
    city: str
    country: str
    postal_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    rating: Optional[float]
    type: Optional[str]
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# ----------------- Room Schema -----------------
class RoomCreate(BaseModel):
    hotel_id: int
    name: str
    room_number: str
    floor_number: Optional[str]
    description: Optional[str]
    type: Optional[str]
    qualification: Optional[str]
    capacity: int
    bed_count: Optional[int]
    price_per_night: float

# New RoomUpdate schema
class RoomUpdate(BaseModel):
    hotel_id: Optional[int]
    name: Optional[str]
    room_number: Optional[str]
    floor_number: Optional[str]
    description: Optional[str]
    type: Optional[str]
    qualification: Optional[str]
    capacity: Optional[int]
    bed_count: Optional[int]
    price_per_night: Optional[condecimal(max_digits=10, decimal_places=2)]
    status: Optional[str]

    class Config:
        orm_mode = True

class Room(BaseModel):
    id: int
    hotel_id: int
    name: str
    room_number: str
    floor_number: Optional[str]
    description: Optional[str]
    type: Optional[str]
    qualification: Optional[str]
    capacity: int
    bed_count: Optional[int]
    price_per_night: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
class FacilityBase(BaseModel):
    id: int
    name: str

# Room schema for basic room information
class RoomBase(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    price: float
    capacity: int

# Hotel schema for hotel information
class HotelBase(BaseModel):
    id: int
    merchant_id: int
    name: str
    description: Optional[str] = None
    address: str
    city: str
    country: str
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    rating: Optional[int] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    status: str

# Merchant schema for merchant information
class MerchantBase(BaseModel):
    id: int
    name: str
    address: str
    phone: str

class ImageBase(BaseModel):
    id: int
    imageable_type: str  # 'hotel' or 'room'
    imageable_id: int    # The ID of the associated hotel or room
    url: str             # URL of the image
    class Config:
        orm_mode = True
class Hotels(BaseModel):
    id: int
    merchant_id: int
    name: str
    description: Optional[str]
    address: str
    city: str
    country: str
    postal_code: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    rating: Optional[float]
    type: Optional[str]
    check_in_time: Optional[str]
    check_out_time: Optional[str]
    status: str
    image: str
    min_price: int
    max_price: int
    facilities: list[FacilityBase]
    class Config:
        orm_mode = True

class RoomDetails(RoomBase):
    # room: RoomBase
    image: ImageBase
    hotel: HotelBase
    facilities: list[FacilityBase]
    merchant: MerchantBase

    class Config:
        orm_mode = True

class RoomDetails2(BaseModel):
    id: int
    hotel_id: int
    name: str
    room_number: str
    floor_number: Optional[str]
    description: Optional[str]
    type: Optional[str]
    qualification: Optional[str]
    capacity: int
    bed_count: Optional[int]
    price_per_night: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    image: str
    facilities: list[FacilityBase]

    class Config:
        orm_mode = True

class HotelDetails(HotelBase):
    image: ImageBase
    merchant: MerchantBase
    room: list[RoomDetails2]

    class Config:
        orm_mode = True
# ----------------- Booking Schema -----------------
class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    check_in_date: datetime
    check_out_date: datetime
    guest_count: int
    total_price: float
    special_requests: Optional[str] = None

# BookingUpdate schema (for updating an existing booking)
class BookingUpdate(BaseModel):
    check_in_date: Optional[datetime] = None
    check_out_date: Optional[datetime] = None
    guest_count: Optional[int] = None
    total_price: Optional[float] = None
    special_requests: Optional[str] = None
    status: Optional[str] = None  # Status can be updated

    class Config:
        orm_mode = True

class Booking(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in_date: datetime
    check_out_date: datetime
    guest_count: int
    total_price: float
    special_requests: Optional[str]
    qr_code: Optional[str]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# ----------------- Payment Schema -----------------
class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    payment_method: str = Field(..., regex="^(credit_card|bank_transfer|e_wallet)$")


class Payment(BaseModel):
    id: int
    booking_id: int
    amount: float
    payment_method: str
    transaction_id: Optional[str]
    status: str
    paid_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# ----------------- Access Log Schema -----------------
class AccessLogCreate(BaseModel):
    booking_id: int
    room_id: int
    action: str = Field(..., regex="^(door_open|door_close|qr_scan)$")
    status: str = Field(..., regex="^(success|failed)$")
    error_message: Optional[str] = None


class AccessLog(BaseModel):
    id: int
    booking_id: int
    room_id: int
    action: str
    status: str
    error_message: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

# ----------------- Review Schema -----------------
class ReviewCreate(BaseModel):
    booking_id: int
    user_id: int
    room_id: int
    rating: int
    comment: Optional[str] = None


class Review(BaseModel):
    id: int
    booking_id: int
    user_id: int
    room_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# ----------------- Help Desk Ticket Schema -----------------
class HelpDeskTicketCreate(BaseModel):
    user_id: int
    booking_id: Optional[int] = None
    title: str
    description: str
    priority: str = Field("low", regex="^(low|medium|high)$")


class HelpDeskTicket(BaseModel):
    id: int
    user_id: int
    booking_id: Optional[int]
    title: str
    description: str
    priority: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# FacilityCreate schema (to create a new facility)
class FacilityCreate(BaseModel):
    name: str
    icon: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

# Facility schema (for response model)
class Facility(FacilityCreate):
    id: int

    class Config:
        orm_mode = True

class FacilityUpdate(BaseModel):
    name: Optional[str]
    icon: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

# RoomFacilityCreate schema (for creating a room-facility relationship)
class RoomFacilityCreate(BaseModel):
    room_id: int
    facility_id: int

    class Config:
        orm_mode = True

# RoomFacility schema (for returning room-facility relationship)
class RoomFacility(RoomFacilityCreate):
    id: int

    class Config:
        orm_mode = True

# ImageCreate schema (for creating a new image record)
class ImageCreate(BaseModel):
    imageable_type: str  # 'hotel' or 'room'
    imageable_id: int    # The ID of the associated hotel or room
    url: str             # URL of the image
    is_primary: Optional[bool] = False  # Whether the image is the primary image

    class Config:
        orm_mode = True



# Image schema (for returning image record)
class Image(ImageCreate):
    id: int  # The ID of the image (auto-generated)

    class Config:
        orm_mode = True