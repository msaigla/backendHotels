from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
            self,
            description: str,
            title: str,
            hotel_id: int,
            limit: int,
            offset: int
    ) -> list[Room]:
        query = select(RoomsOrm)
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if hotel_id is not None:
            query = query.filter_by(hotel_id=hotel_id)
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        """
        with rooms_count as (
            select room_id, count(*) as rooms_booked from bookings
            where date_from <= '2024-11-07' and date_to >= '2024-07-01'
            group by room_id
        ),
        rooms_left_table as (
            select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
            from rooms
            left join rooms_count on rooms.id = rooms_count.room_id
        )
        select * from rooms_left_table
        where rooms_left > 0;
        """

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
