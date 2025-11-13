from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_USER = os.getenv("DB_USER","admin")
DB_PASS = os.getenv("DB_PASS","Chinook123!")
DB_HOST = os.getenv("DB_HOST","<RDS_ENDPOINT>")
DB_NAME = os.getenv("DB_NAME","Chinook")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
