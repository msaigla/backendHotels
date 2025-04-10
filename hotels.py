from fastapi import APIRouter, Query, Body

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Столы"])

hotels = [
     {"id": 1, "title": "Sochi", "description": "sochi"},
     {"id": 2, "title": "Дубай", "description": "dubai"},
     {"id": 3, "title": "Мальдивы", "description": "maldivi"},
     {"id": 4, "title": "Геленджик", "description": "gelendzhik"},
     {"id": 5, "title": "Москва", "description": "moscow"},
     {"id": 6, "title": "Казань", "description": "kazan"},
     {"id": 7, "title": "Санкт-Петербург", "description": "spb"},
 ]


@router.get("")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(None),
        per_page: int | None = Query(None),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if page is None:
        page = 1
    if per_page is None:
        per_page = 3
    return hotels_[(page - 1) * per_page:(page) * per_page]


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "Сочи": {"summery": "Сочи", "value": {
        "title": "Отель сочи 5 звезд у моря",
        "description": "Сочи у моря",
    }},
    "Дубай": {"summery": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "description": "дубай у фонтана",
    }},
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "description": hotel_data.description
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["description"] = hotel_data.description
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def edit_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.description:
                hotel["description"] = hotel_data.description
    return {"status": "OK"}
