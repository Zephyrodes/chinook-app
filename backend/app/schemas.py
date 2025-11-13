from typing import List, Optional
from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime

class ArtistOut(BaseModel):
    ArtistId: int
    Name: str

    class Config:
        orm_mode = True

class TrackOut(BaseModel):
    TrackId: int
    Name: str
    UnitPrice: condecimal(max_digits=10, decimal_places=2)
    AlbumId: Optional[int]
    GenreId: Optional[int]
    MediaTypeId: int

    class Config:
        orm_mode = True

class PurchaseLine(BaseModel):
    track_id: int
    quantity: int = 1

class PurchaseRequest(BaseModel):
    customer_id: int
    lines: List[PurchaseLine]
    billing_address: Optional[str] = None
    billing_city: Optional[str] = None
    billing_country: Optional[str] = None

class PurchaseResponse(BaseModel):
    invoice_id: int
    total: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime
