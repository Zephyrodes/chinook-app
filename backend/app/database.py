import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]
DB_POOL_SIZE = int(os.environ.get("DB_POOL_SIZE", 10))
DB_MAX_OVERFLOW = int(os.environ.get("DB_MAX_OVERFLOW", 20))
DB_POOL_TIMEOUT = int(os.environ.get("DB_POOL_TIMEOUT", 30))
SQL_ECHO = os.environ.get("SQL_ECHO", "false").lower() == "true"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_timeout=DB_POOL_TIMEOUT,
    echo=SQL_ECHO
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
