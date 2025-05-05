from fastapi import APIRouter, Request

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException, UserNotAuthHTTPException, \
    RoomNotFoundException, RoomNotFoundHTTPException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep, request: Request):
    if not request.cookies.get("access_token"):
        raise UserNotAuthHTTPException
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
        request: Request
):
    if not request.cookies.get("access_token"):
        raise UserNotAuthHTTPException
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK", "data": booking}
