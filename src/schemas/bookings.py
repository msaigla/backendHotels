from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BookingAddRequest):
    price: int
    user_id: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
