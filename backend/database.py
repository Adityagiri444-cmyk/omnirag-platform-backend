from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - now using PostgreSQL
DATABASE_URL = "postgresql://postgres:Aditya%4065@localhost:5432/omnirag_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency - gives database session to each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()