from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("/")
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("/")
async def add_facility(db: DBDep, data: FacilitiesAdd):
    data = await db.facilities.add(data)
    await db.commit()
    return {
        "status": "ok",
        "data": data
    }


