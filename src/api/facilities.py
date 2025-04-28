from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import task_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
# @cache(expire=10)
async def get_facilities(db: DBDep):
    print("иду в базу данных")
    return await db.facilities.get_all()


@router.post("")
async def add_facility(db: DBDep, data: FacilityAdd = Body()):
    data = await db.facilities.add(data)
    await db.commit()

    task_task.delay()

    return {
        "status": "ok",
        "data": data
    }


