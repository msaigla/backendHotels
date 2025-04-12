from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def create_hotel(
        db: DBDep,
        user_id: UserIdDep,
        data: BookingAddRequest
):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(status_code=401, detail="Такой комнаты нету")
    room_price: int = room.price
    _data = BookingAdd(price=room_price, user_id=user_id, **data.dict())
    booking = await db.bookings.add(_data)
    await db.commit()
    return {"status": "OK", "data": booking}
