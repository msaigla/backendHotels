from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def add_facility(db: DBDep, data: FacilityAdd = Body()):
    facility = await FacilityService(db).add_facility(data)

    return {"status": "ok", "data": facility}
