from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):

    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facility(self, data: FacilityAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()  # type: ignore
        return facility
