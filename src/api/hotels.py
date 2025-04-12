from fastapi import APIRouter, Query, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=(pagination.page - 1) * per_page,
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "ул. Шейха, 2",
                },
            },
        }),
):
    return {"status": "OK", "data": await db.hotels.add(hotel_data)}


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    return {"status": "OK"}
