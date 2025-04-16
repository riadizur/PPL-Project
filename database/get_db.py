from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace 'sqlite:///example.db' with your actual database URL
DATABASE_URL = "sqlite:///./data/hotel_booking.db"

# Create an engine instance
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()