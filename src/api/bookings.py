from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings_me(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=400, detail="Room not found")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.dict(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
