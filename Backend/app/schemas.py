from pydantic import BaseModel
from datetime import datetime

class ItemBase(BaseModel):
    type: str
    brand: str
    confidence: float
    decision: str
    reasoning: str

class ItemCreate(ItemBase):
    image_path: str

class ItemRead(ItemBase):
    id: int
    image_path: str
    timestamp: datetime

    class Config:
        orm_mode = True
