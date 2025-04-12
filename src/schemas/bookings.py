from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAdd(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingFull(BookingAdd):
    price: int
    user_id: int


class Booking(BookingFull):
    price: int
    user_id: int
    id: int

    model_config = ConfigDict(from_attributes=True)
