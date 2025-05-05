from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import (HotelNotFoundHTTPException,
                            RoomNotFoundHTTPException,
                            RoomNotFoundException,
                            HotelNotFoundException)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/rooms", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
):
    try:
        return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).get_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundException
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_patch(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    try:
        await RoomService(db).edit_room_patch(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundException
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundException
    return {"status": "OK"}
