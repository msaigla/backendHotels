from datetime import date

from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep, DBDep
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
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
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
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {
                "summary": "Комната в сочи",
                "value": {
                    "title": "Комната 1",
                    "hotel_id": 19,
                    "description": "С окном видом на море",
                    "price": 2000,
                    "quantity": 2
                },
            },
            "2": {
                "summary": "Комната в дубае",
                "value": {
                    "title": "Комната 1",
                    "hotel_id": 20,
                    "description": "С окном балконом видом во двор",
                    "price": 1500,
                    "quantity": 2
                },
            },
        }),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    data = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": data}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(
        data=_room_data,
        id=room_id
    )
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def edit_room(db: DBDep, hotel_id, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
