import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Use DATABASE_URL env var, e.g.:
# mysql+pymysql://user:password@host:3306/chinook
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")  # fallback safe local

# Important engine options for production MySQL on AWS RDS
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
    pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
    echo=(os.getenv("SQL_ECHO", "false").lower() == "true"),
)

# Session factory and Base class for models
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

def get_db():
    """
    Dependency for FastAPI endpoints.
    Yields a SQLAlchemy session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
