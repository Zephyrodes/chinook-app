# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_size=int(os.environ.get("DB_POOL_SIZE", 10)),
    max_overflow=int(os.environ.get("DB_MAX_OVERFLOW", 20)),
    pool_timeout=int(os.environ.get("DB_POOL_TIMEOUT", 30)),
    echo=os.environ.get("SQL_ECHO", "false").lower() == "true"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# --- Agregar get_db ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
