from src.models.facilities import FacilitiesOrm
from src.repos.base import BaseRepository
from src.schemas.facilities import Facilities
from src.schemas.rooms import Room


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities
