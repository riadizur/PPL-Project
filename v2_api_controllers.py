from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
import v2_models, v2_schemas
from v2_database import SessionLocal, engine
from sqlalchemy import or_

# Dependency to get the current session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT settings
SECRET_KEY = "ppl-project"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI OAuth2 bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password encryption context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create FastAPI router instance
router = APIRouter()

# Utility function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)

# Utility function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Utility function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Utility function to get current user from JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = db.query(v2_models.User).filter(v2_models.User.id == user_id).first()
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user

# Register a new user
@router.post("/register", response_model=v2_schemas.User)
async def register(user: v2_schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(v2_models.User).filter(
        (v2_models.User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user.password)
    db_user = v2_models.User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        phone=user.phone,
        role=user.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Login and get JWT token
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(v2_models.User).filter(v2_models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# CRUD operations for users
@router.get("/users", response_model=List[v2_schemas.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(v2_models.User).all()

@router.get("/users/{user_id}", response_model=v2_schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(v2_models.User).filter(v2_models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=v2_schemas.User)
def update_user(user_id: int, user: v2_schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(v2_models.User).filter(v2_models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password:
        db_user.password = hash_password(user.password)
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(v2_models.User).filter(v2_models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"msg": "User deleted successfully"}

# CRUD operations for merchants
@router.post("/merchants", response_model=v2_schemas.Merchant)
def create_merchant(merchant: v2_schemas.MerchantCreate, db: Session = Depends(get_db)):
    merchant = {
        "user_id": merchant.user_id,
        "company_name": merchant.company_name,
        "business_license": merchant.business_license,
        "tax_number": merchant.tax_number,
        "address": merchant.address
    }
    db_merchant = v2_models.Merchant(**merchant.dict())
    db.add(db_merchant)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant

@router.get("/merchants", response_model=List[v2_schemas.Merchant])
def get_merchants(db: Session = Depends(get_db)):
    return db.query(v2_models.Merchant).all()

@router.get("/merchants/{merchant_id}", response_model=v2_schemas.Merchant)
def get_merchant(merchant_id: int, db: Session = Depends(get_db)):
    db_merchant = db.query(v2_models.Merchant).filter(v2_models.Merchant.id == merchant_id).first()
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return db_merchant

@router.put("/merchants/{merchant_id}", response_model=v2_schemas.Merchant)
def update_merchant(merchant_id: int, merchant: v2_schemas.MerchantUpdate, db: Session = Depends(get_db)):
    db_merchant = db.query(v2_models.Merchant).filter(v2_models.Merchant.id == merchant_id).first()
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    for key, value in merchant.dict(exclude_unset=True).items():
        setattr(db_merchant, key, value)
    db.commit()
    db.refresh(db_merchant)
    return db_merchant

@router.delete("/merchants/{merchant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_merchant(merchant_id: int, db: Session = Depends(get_db)):
    db_merchant = db.query(v2_models.Merchant).filter(v2_models.Merchant.id == merchant_id).first()
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    db.delete(db_merchant)
    db.commit()
    return {"msg": "Merchant deleted successfully"}

# CRUD operations for hotels
@router.post("/hotels", response_model=v2_schemas.Hotel)
def create_hotel(hotel: v2_schemas.HotelCreate, db: Session = Depends(get_db)):
    db_hotel = v2_models.Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel
@router.get("/hotel", response_model=List[v2_schemas.Hotel])
def get_hotel(db: Session = Depends(get_db)):
    return db.query(v2_models.Hotel).all()

@router.get("/hotel/{hotel_id}", response_model=v2_schemas.Hotel)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = db.query(v2_models.Hotel).filter(v2_models.Hotel.id == hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return db_hotel

@router.get("/hotels", response_model=List[v2_schemas.Hotels])
def get_hotels(db: Session = Depends(get_db)):
    hotels = db.query(v2_models.Hotel).all()
    result = []
    
    for hotel in hotels:
        image = db.query(v2_models.Image).filter(v2_models.Image.imageable_id == hotel.id).first()
        room_prices = db.query(v2_models.Room.price_per_night).filter(v2_models.Room.hotel_id == hotel.id).all()
        if room_prices:
            min_price = min([price[0] for price in room_prices])
            max_price = max([price[0] for price in room_prices])
        else:
            min_price = max_price = 0
        facility_ids = db.query(v2_models.Room.id).filter(v2_models.Room.hotel_id == hotel.id).distinct().all()
        room_facilities = db.query(v2_models.Facility).join(v2_models.RoomFacility).filter(v2_models.RoomFacility.room_id.in_([f[0] for f in facility_ids])).all()
        # room_facilities = db.query(v2_models.RoomFacility).filter(v2_models.RoomFacilitRoomFacilityyCreate.room_id.in_([f[0] for f in facility_ids])).all()
        facilities_data = [v2_schemas.FacilityBase(id=facility.id, name=facility.name) for facility in room_facilities]
        
        result.append({
            "id": hotel.id,
            "merchant_id": hotel.merchant_id,
            "name": hotel.name,
            "description": hotel.description,
            "address": hotel.address,
            "city": hotel.city,
            "country": hotel.country,
            "postal_code": hotel.postal_code,
            "phone": hotel.phone,
            "email": hotel.email,
            "rating": hotel.rating,
            "type": hotel.type,
            "check_in_time": hotel.check_in_time,
            "check_out_time": hotel.check_out_time,
            "status": hotel.status,
            "image": image.url,
            "min_price": min_price,
            "max_price": max_price,
            "facilities":facilities_data
        })
    return result

@router.get("/hotels/{hotel_id}", response_model=v2_schemas.Hotels)
def get_hotels(hotel_id: int,db: Session = Depends(get_db)):
    hotel = db.query(v2_models.Hotel).filter(v2_models.Hotel.id == hotel_id).first()

    image = db.query(v2_models.Image).filter(v2_models.Image.imageable_id == hotel.id).first()
    room_prices = db.query(v2_models.Room.price_per_night).filter(v2_models.Room.hotel_id == hotel.id).all()
    if room_prices:
        min_price = min([price[0] for price in room_prices])
        max_price = max([price[0] for price in room_prices])
    else:
        min_price = max_price = 0
    facility_ids = db.query(v2_models.Room.id).filter(v2_models.Room.hotel_id == hotel.id).distinct().all()
    room_facilities = db.query(v2_models.Facility).join(v2_models.RoomFacility).filter(v2_models.RoomFacility.room_id.in_([f[0] for f in facility_ids])).all()
    # room_facilities = db.query(v2_models.RoomFacility).filter(v2_models.RoomFacilitRoomFacilityyCreate.room_id.in_([f[0] for f in facility_ids])).all()
    facilities_data = [v2_schemas.FacilityBase(id=facility.id, name=facility.name) for facility in room_facilities]
    return {
        "id": hotel.id,
        "merchant_id": hotel.merchant_id,
        "name": hotel.name,
        "description": hotel.description,
        "address": hotel.address,
        "city": hotel.city,
        "country": hotel.country,
        "postal_code": hotel.postal_code,
        "phone": hotel.phone,
        "email": hotel.email,
        "rating": hotel.rating,
        "type": hotel.type,
        "check_in_time": hotel.check_in_time,
        "check_out_time": hotel.check_out_time,
        "status": hotel.status,
        "image": image.url,
        "min_price": min_price,
        "max_price": max_price,
        "facilities":facilities_data
    }

@router.put("/hotels/{hotel_id}", response_model=v2_schemas.Hotel)
def update_hotel(hotel_id: int, hotel: v2_schemas.HotelUpdate, db: Session = Depends(get_db)):
    db_hotel = db.query(v2_models.Hotel).filter(v2_models.Hotel.id == hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    for key, value in hotel.dict(exclude_unset=True).items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.delete("/hotels/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = db.query(v2_models.Hotel).filter(v2_models.Hotel.id == hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(db_hotel)
    db.commit()
    return {"msg": "Hotel deleted successfully"}

# Continue CRUD for other tables such as rooms, facilities, bookings, payments, access logs, reviews, etc.

# CRUD operations for rooms
@router.post("/rooms", response_model=v2_schemas.Room)
def create_room(room: v2_schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = v2_models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/rooms", response_model=List[v2_schemas.Room])
def get_rooms(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    room_type: Optional[str] = None,
    qualification: Optional[str] = None,
    check_in_date: Optional[datetime] = None,
    check_out_date: Optional[datetime] = None,
):
    query = db.query(v2_models.Room)
    if min_price:
        query = query.filter(v2_models.Room.price_per_night >= min_price)
    if max_price:
        query = query.filter(v2_models.Room.price_per_night <= max_price)
    if room_type:
        query = query.filter(v2_models.Room.type == room_type)
    if qualification:
        query = query.filter(v2_models.Room.qualification == qualification)

    # Filtering rooms based on availability for the specified date range
    if check_in_date and check_out_date:
        unavailable_rooms = (
            db.query(v2_models.Booking.room_id)
            .filter(
                or_(
                    v2_models.Booking.check_in_date.between(check_in_date, check_out_date),
                    v2_models.Booking.check_out_date.between(check_in_date, check_out_date),
                )
            )
            .distinct()
        )
        query = query.filter(v2_models.Room.id.notin_(unavailable_rooms))

    return query.offset(offset).limit(limit).all()

@router.get("/rooms/{room_id}", response_model=v2_schemas.Room)
def get_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(v2_models.Room).filter(v2_models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.put("/rooms/{room_id}", response_model=v2_schemas.Room)
def update_room(room_id: int, room: v2_schemas.RoomUpdate, db: Session = Depends(get_db)):
    db_room = db.query(v2_models.Room).filter(v2_models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    for key, value in room.dict(exclude_unset=True).items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(v2_models.Room).filter(v2_models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"msg": "Room deleted successfully"}

@router.get("/rooms_details/{room_id}", response_model=v2_schemas.RoomDetails)
async def get_room_details(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(v2_models.Room).filter(v2_models.Room.id == room_id).first()

    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")

    db_hotel = db.query(v2_models.Hotel).filter(v2_models.Hotel.id == db_room.hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    room_facilities = db.query(v2_models.Facility).join(v2_models.RoomFacility).filter(v2_models.RoomFacility.room_id == db_room.id).all()
    db_merchant = db.query(v2_models.Merchant).filter(v2_models.Merchant.id == db_hotel.merchant_id).first()
    db_image = db.query(v2_models.Image).filter(v2_models.Image.imageable_id == db_room.id).first()
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    # Construct the response using Pydantic models
    room_data = v2_schemas.RoomBase(
        id=db_room.id,
        hotel_id=db_room.hotel_id,
        name=db_room.name,
        description=db_room.description,
        price=db_room.price_per_night,
        capacity=db_room.capacity
    )
    # return room_data

    hotel_data = v2_schemas.HotelBase(
        id=db_hotel.id,
        merchant_id=db_hotel.merchant_id,
        name=db_hotel.name,
        description=db_hotel.description,
        address=db_hotel.address,
        city=db_hotel.city,
        country=db_hotel.country,
        postal_code=db_hotel.postal_code,
        phone=db_hotel.phone,
        email=db_hotel.email,
        rating=db_hotel.rating,
        check_in_time=db_hotel.check_in_time,
        check_out_time=db_hotel.check_out_time,
        status=db_hotel.status
    )

    facilities_data = [v2_schemas.FacilityBase(id=facility.id, name=facility.name) for facility in room_facilities]

    merchant_data = v2_schemas.MerchantBase(
        id=db_merchant.id,
        name=db_merchant.company_name,
        address=db_merchant.address,
        phone=db_merchant.phone
    )
    image_data = v2_schemas.ImageBase(
        id=db_image.id,
        imageable_type=db_image.imageable_type,
        imageable_id=db_image.imageable_id,
        url=db_image.url
    )

    return {
        "id": room_data.id,
        "hotel_id": room_data.hotel_id,
        "name": room_data.name,
        "description": room_data.description,
        "price": room_data.price,
        "capacity": room_data.capacity,
        "image": image_data,
        "hotel": hotel_data,
        "facilities": facilities_data,
        "merchant": merchant_data,
    }

@router.get("/hotels_details/{hotel_id}", response_model=v2_schemas.HotelDetails)
async def get_hotel_details(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = db.query(v2_models.Hotel).filter(v2_models.Hotel.id == hotel_id).first()

    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    db_merchant = db.query(v2_models.Merchant).filter(v2_models.Merchant.id == db_hotel.merchant_id).first()
    db_image = db.query(v2_models.Image).filter(v2_models.Image.imageable_id == db_hotel.id).first()
    db_room = db.query(v2_models.Room).filter(v2_models.Room.hotel_id == db_hotel.id).all()
    if not db_merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    room_data = []
    for room in db_room :
        room_facilities = db.query(v2_models.Facility).join(v2_models.RoomFacility).filter(v2_models.RoomFacility.room_id == room.id).all()
        # db_image_room = db.query(v2_models.Image).filter(v2_models.Image.imageable_id == room.id).first()
        hotel_data = v2_schemas.HotelBase(
            id=db_hotel.id,
            merchant_id=db_hotel.merchant_id,
            name=db_hotel.name,
            description=db_hotel.description,
            address=db_hotel.address,
            city=db_hotel.city,
            country=db_hotel.country,
            postal_code=db_hotel.postal_code,
            phone=db_hotel.phone,
            email=db_hotel.email,
            rating=db_hotel.rating,
            check_in_time=db_hotel.check_in_time,
            check_out_time=db_hotel.check_out_time,
            status=db_hotel.status
        )

        facilities_data = [v2_schemas.FacilityBase(id=facility.id, name=facility.name) for facility in room_facilities]

        merchant_data = v2_schemas.MerchantBase(
            id=db_merchant.id,
            name=db_merchant.company_name,
            address=db_merchant.address,
            phone=db_merchant.phone
        )
        # image_data = v2_schemas.ImageBase(
        #     id=db_image_room.id,
        #     imageable_type=db_image_room.imageable_type,
        #     imageable_id=db_image_room.imageable_id,
        #     url=db_image.url
        # )
        room_data.append({
            "id":room.id,
            "hotel_id":room.hotel_id,
            "name":room.name,
            "room_number":room.room_number,
            "floor_number":room.floor_number,
            "description":room.description,
            "type":room.type,
            "qualification":room.qualification,
            "capacity":room.capacity,
            "bed_count":room.bed_count,
            "price_per_night":room.price_per_night,
            "status":room.status,
            "created_at":room.created_at,
            "updated_at":room.updated_at,
            "image": db_image.url,
            "facilities": facilities_data,
        })
    # room_data = [v2_schemas.Room(id=room.id,hotel_id=room.hotel_id,name=room.name,room_number=room.room_number,floor_number=room.floor_number,description=room.description,type=room.type,qualification=room.qualification,capacity=room.capacity,bed_count=room.bed_count,price_per_night=room.price_per_night,status=room.status,created_at=room.created_at,updated_at=room.updated_at) for room in db_room]
    # print(room_data)
    return {
        "id": db_hotel.id,
        "merchant_id": db_hotel.merchant_id,
        "name": db_hotel.name,
        "description": db_hotel.description,
        "address": db_hotel.address,
        "city": db_hotel.city,
        "country": db_hotel.country,
        "postal_code": db_hotel.postal_code,
        "phone": db_hotel.phone,
        "email": db_hotel.email,
        "rating": db_hotel.rating,
        "check_in_time": db_hotel.check_in_time,
        "check_out_time": db_hotel.check_out_time,
        "status": db_hotel.status,
        "image":db_image,
        "merchant": merchant_data,
        "room": room_data,
    }

# CRUD operations for facilities
@router.post("/facilities", response_model=v2_schemas.Facility)
def create_facility(facility: v2_schemas.FacilityCreate, db: Session = Depends(get_db)):
    db_facility = v2_models.Facility(**facility.dict())
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility

@router.get("/facilities", response_model=List[v2_schemas.Facility])
def get_facilities(db: Session = Depends(get_db)):
    return db.query(v2_models.Facility).all()

@router.get("/facilities/{facility_id}", response_model=v2_schemas.Facility)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    db_facility = db.query(v2_models.Facility).filter(v2_models.Facility.id == facility_id).first()
    if not db_facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return db_facility

@router.put("/facilities/{facility_id}", response_model=v2_schemas.Facility)
def update_facility(facility_id: int, facility: v2_schemas.FacilityUpdate, db: Session = Depends(get_db)):
    db_facility = db.query(v2_models.Facility).filter(v2_models.Facility.id == facility_id).first()
    if not db_facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    for key, value in facility.dict(exclude_unset=True).items():
        setattr(db_facility, key, value)
    db.commit()
    db.refresh(db_facility)
    return db_facility

@router.delete("/facilities/{facility_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_facility(facility_id: int, db: Session = Depends(get_db)):
    db_facility = db.query(v2_models.Facility).filter(v2_models.Facility.id == facility_id).first()
    if not db_facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    db.delete(db_facility)
    db.commit()
    return {"msg": "Facility deleted successfully"}

# CRUD operations for room_facilities
@router.post("/room_facilities", response_model=v2_schemas.RoomFacility)
def create_room_facility(room_facility: v2_schemas.RoomFacilityCreate, db: Session = Depends(get_db)):
    db_room_facility = v2_models.RoomFacility(**room_facility.dict())
    db.add(db_room_facility)
    db.commit()
    db.refresh(db_room_facility)
    return db_room_facility

@router.get("/room_facilities", response_model=List[v2_schemas.RoomFacility])
def get_room_facilities(db: Session = Depends(get_db)):
    return db.query(v2_models.RoomFacility).all()

@router.delete("/room_facilities/{room_facility_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room_facility(room_facility_id: int, db: Session = Depends(get_db)):
    db_room_facility = db.query(v2_models.RoomFacility).filter(v2_models.RoomFacility.id == room_facility_id).first()
    if not db_room_facility:
        raise HTTPException(status_code=404, detail="Room Facility not found")
    db.delete(db_room_facility)
    db.commit()
    return {"msg": "Room Facility deleted successfully"}

# CRUD operations for images
@router.post("/images", response_model=v2_schemas.Image)
def create_image(image: v2_schemas.ImageCreate, db: Session = Depends(get_db)):
    db_image = v2_models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

@router.get("/images", response_model=List[v2_schemas.Image])
def get_images(db: Session = Depends(get_db)):
    return db.query(v2_models.Image).all()

@router.get("/images/{image_id}", response_model=v2_schemas.Image)
def get_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(v2_models.Image).filter(v2_models.Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = db.query(v2_models.Image).filter(v2_models.Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(db_image)
    db.commit()
    return {"msg": "Image deleted successfully"}

# CRUD operations for bookings
@router.post("/bookings", response_model=v2_schemas.Booking)
def create_booking(booking: v2_schemas.BookingCreate, db: Session = Depends(get_db)):
    db_booking = v2_models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/bookings", response_model=List[v2_schemas.Booking])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(v2_models.Booking).all()

@router.get("/bookings/{booking_id}", response_model=v2_schemas.Booking)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(v2_models.Booking).filter(v2_models.Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.put("/bookings/{booking_id}", response_model=v2_schemas.Booking)
def update_booking(booking_id: int, booking: v2_schemas.BookingUpdate, db: Session = Depends(get_db)):
    db_booking = db.query(v2_models.Booking).filter(v2_models.Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    for key, value in booking.dict(exclude_unset=True).items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.delete("/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(v2_models.Booking).filter(v2_models.Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return {"msg": "Booking deleted successfully"}

# CRUD operations for payments
@router.post("/payments", response_model=v2_schemas.Payment)
def create_payment(payment: v2_schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = v2_models.Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/payments", response_model=List[v2_schemas.Payment])
def get_payments(db: Session = Depends(get_db)):
    return db.query(v2_models.Payment).all()

@router.get("/payments/{payment_id}", response_model=v2_schemas.Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(v2_models.Payment).filter(v2_models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(v2_models.Payment).filter(v2_models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()
    return {"msg": "Payment deleted successfully"}

# CRUD operations for access_logs
@router.post("/access_logs", response_model=v2_schemas.AccessLog)
def create_access_log(access_log: v2_schemas.AccessLogCreate, db: Session = Depends(get_db)):
    db_access_log = v2_models.AccessLog(**access_log.dict())
    db.add(db_access_log)
    db.commit()
    db.refresh(db_access_log)
    return db_access_log

@router.get("/access_logs", response_model=List[v2_schemas.AccessLog])
def get_access_logs(db: Session = Depends(get_db)):
    return db.query(v2_models.AccessLog).all()

@router.delete("/access_logs/{access_log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_access_log(access_log_id: int, db: Session = Depends(get_db)):
    db_access_log = db.query(v2_models.AccessLog).filter(v2_models.AccessLog.id == access_log_id).first()
    if not db_access_log:
        raise HTTPException(status_code=404, detail="Access Log not found")
    db.delete(db_access_log)
    db.commit()
    return {"msg": "Access Log deleted successfully"}

# CRUD operations for reviews
@router.post("/reviews", response_model=v2_schemas.Review)
def create_review(review: v2_schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_review = v2_models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/reviews", response_model=List[v2_schemas.Review])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(v2_models.Review).all()

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(v2_models.Review).filter(v2_models.Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"msg": "Review deleted successfully"}

import qrcode

@router.post("/hardware/door-access")
async def control_door(access_log: v2_schemas.AccessLogCreate, db: Session = Depends(get_db)):
    try:
        db_access_log = v2_models.AccessLog(**access_log.dict())
        db.add(db_access_log)
        db.commit()
        db.refresh(db_access_log)
        return {"message": f"Door successfully {access_log.action}ed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class QRValidateRequest(v2_schemas.BaseModel):
    qr_code: str
    room_id: int

class QRGenerateRequest(v2_schemas.BaseModel):
    booking_id: int
    room_id: int

@router.post("/hardware/qr/validate")
async def validate_qr(request: QRValidateRequest, db: Session = Depends(get_db)):
    booking = db.query(v2_models.Booking).filter(
        v2_models.Booking.qr_code == request.qr_code,
        v2_models.Booking.room_id == request.room_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking data not found")
    return {"valid": True, "data":booking}


import json
@router.post("/hardware/qr/generate")
async def generate_qr(
    request: QRGenerateRequest,
    db: Session = Depends(get_db)
):
    # try:
    # booking = db.query(v2_models.Booking).filter(
    #     v2_models.Booking.id == request.booking_id,
    #     v2_models.Booking.room_id == request.room_id
    # ).first()

    # if not booking:
    #     raise HTTPException(status_code=422, detail="Booking not found")

    # Generate QR code
    qr_data = {
        "booking_id": request.booking_id,
        "room_id": request.room_id,
        "timestamp": datetime.now().isoformat()
    }
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    # Generate unique QR code string
    qr_string = f"QR_{request.booking_id,}_{datetime.now().timestamp()}"
    
    # Update booking with QR code
    # booking.qr_code = qr_string
    
    db.commit()
    
    return {
        "qr_code": qr_string
    }

    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=422, detail=str(e))