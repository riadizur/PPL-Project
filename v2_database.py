from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL; this example uses SQLite
DATABASE_URL = "sqlite:///./data/v2_hotel.db"  # Adjust the path if needed

# Create an engine to handle database connections
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal class, each instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class to use for models
Base = declarative_base()

# Dependency to get DB session, used in FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()