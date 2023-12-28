from pydantic import EmailStr
from sqlalchemy import RowMapping

from app.base.crud import BaseCRUD
from app.users.models import User


class UserCRUD(BaseCRUD):
    model = User

    @classmethod
    async def select_by_email_or_none(cls, email: EmailStr) -> RowMapping | None:
        result = await cls._select_basic(email=email)
        return result.mappings().one_or_none()
