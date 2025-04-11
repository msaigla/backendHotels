from fastapi import APIRouter
from sqlalchemy.testing.pickleable import User

from repos.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация т аутентификация"])


@router.post("/register")
async def register(
        data: UserRequestAdd
):
    hashed_password = "dawkldjioawje3894892r"
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}
