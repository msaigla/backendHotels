from src.models.bookings import BookingsOrm
from src.repos.base import BaseRepository
from src.repos.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
