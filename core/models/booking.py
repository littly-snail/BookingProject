from pydantic import BaseModel
from typing import Optional
from datetime import date


class Bookingdates(BaseModel):
    checkin: date
    checkout: date


class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: Bookingdates
    additionalneeds: Optional[str] = None


class BookingResponse(BaseModel):
    bookingid: int
    booking: Booking