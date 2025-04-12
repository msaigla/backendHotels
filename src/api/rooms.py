from fastapi import APIRouter, Query, Body

from src.repos.rooms import RoomsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.rooms import RoomPATCH, RoomAdd

router = APIRouter(prefix="/rooms", tags=["Комнаты"])


@router.get("")
async def get_rooms(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        description: str | None = Query(None, description="Описание комнаты"),
        hotel_id: int | None = Query(None, description="Айди отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            title=title,
            description=description,
            hotel_id=hotel_id,
            limit=per_page,
            offset=(pagination.page - 1) * per_page,
        )


@router.post("")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.get("/{room_id}")
async def get_room(room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.put("/{room_id}")
async def edit_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{room_id}")
async def edit_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{room_id}")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}
