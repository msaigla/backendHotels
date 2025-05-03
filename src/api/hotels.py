from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (ObjectNotFoundException, HotelNotFoundHTTPException,
                            CreateHotelEmptyFieldsHTTPException,
                            PatchNoFieldsException, PatchNoFieldsHTTPException)
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация"),
        date_from: date = Query(example="2025-08-01"),
        date_to: date = Query(example="2025-08-10"),
):
    return await HotelService(db).get_filtered_by_time(pagination, title, location, date_from, date_to)


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
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
            }
        ),
):
    try:
        hotel = await HotelService(db).add_hotel(hotel_data)
    except ObjectNotFoundException:
        raise CreateHotelEmptyFieldsHTTPException
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def edit_hotel_patch(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    try:
        await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    except PatchNoFieldsException:
        raise PatchNoFieldsHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
