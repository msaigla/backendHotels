from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, DateFromLaterThanDateTo
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
    try:
        return await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
    except DateFromLaterThanDateTo as ex:
        raise HTTPException(status_code=403, detail=ex.detail)
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
    try:
        return await db.rooms.get_one(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номера не существует")


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        data = await db.rooms.add(_room_data)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отеля не существует")
    rooms_facilities_data = [
        RoomsFacilityAdd(room_id=data.id, facility_id=f_id) for f_id in room_data.facilities_ids
    ]
    if rooms_facilities_data:
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": data}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        result = await db.rooms.edit(data=_room_data, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номера не существует")
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "OK", "data": result}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room_patch(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    try:
        await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номера не существует")
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номера не существует")
    await db.commit()
    return {"status": "OK"}
