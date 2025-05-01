from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, check_date_to_is_after_date_from, HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/rooms", tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        # pagination: PaginationDep,
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
        # title: str | None = Query(None, description="Название отеля"),
        # description: str | None = Query(None, description="Описание комнаты"),
):
    check_date_to_is_after_date_from(date_from, date_to)
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    # per_page = pagination.per_page or 5
    # return await db.rooms.get_all(
    #     title=title,
    #     description=description,
    #     hotel_id=hotel_id,
    #     limit=per_page,
    #     offset=(pagination.page - 1) * per_page,
    # )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HTTPException(status_code=404, detail="Номера или отеля не существует")


@router.post("/{hotel_id}/rooms")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    data = await db.rooms.add(_room_data)
    rooms_facilities_data = [
        RoomsFacilityAdd(room_id=data.id, facility_id=f_id) for f_id in room_data.facilities_ids
    ]
    if rooms_facilities_data:
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": data}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        result = await db.rooms.edit(data=_room_data, id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "OK", "data": result}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_patch(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    try:
        await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    await db.commit()
    return {"status": "OK"}
