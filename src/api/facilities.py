from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def add_facility(db: DBDep, data: FacilityAdd = Body()):
    data = await db.facilities.add(data)
    await db.commit()
    return {
        "status": "ok",
        "data": data
    }


