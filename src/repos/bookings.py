from typing import List

from pydantic import BaseModel
from sqlalchemy import select

from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_me(self, user_id: int) -> list[Booking]:
        query = select(self.model).filter_by(user_id=user_id)
        result = await self.session.execute(query)
        return [self.schema.model_validate(booking, from_attributes=True) for booking in result.scalars().all()]
