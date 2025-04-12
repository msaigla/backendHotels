from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingAdd, BookingFull

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_hotel(
        db: DBDep,
        user_id: UserIdDep,
        data: BookingAdd
):
    user = await db.users.get_one_or_none(id=user_id)
    room = await db.rooms.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(status_code=401, detail="Такой комнаты нету")
    price = room.price * (data.date_to - data.date_from).days
    _data = BookingFull(price=price, user_id=user.id, **data.model_dump())
    booking = await db.bookings.add(_data)
    await db.commit()
    return {"status": "OK", "data": booking}
