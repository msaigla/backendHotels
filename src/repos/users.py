from pydantic import EmailStr
from sqlalchemy import select

from src.exceptions import UserExistsEmail
from src.repos.base import BaseRepository
from src.models.users import UsersOrm
from src.repos.mappers.mappers import UserDataMapper
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        try:
            query = select(self.model).filter_by(email=email)
            result = await self.session.execute(query)
            model = result.scalars().one()
        except:
            raise UserExistsEmail
        return UserWithHashedPassword.model_validate(model)
