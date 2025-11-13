from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from app.database import Base

class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(50))
    payload = Column(Text)
    created_at = Column(DateTime)
