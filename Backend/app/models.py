from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from .db import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    type = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    reasoning = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
