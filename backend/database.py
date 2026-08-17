from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - using SQLite for now (no installation needed)
DATABASE_URL = "sqlite:///./omnirag.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency - gives database session to each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()