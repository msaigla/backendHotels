from sqlalchemy import select, func

from src.repos.base import BaseRepository
from src.models.rooms import RoomsOrm
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
