from typing import Any, Mapping, TypeVar

import pydantic
from sqlalchemy import Result, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.base.exceptions import DataBaseError
from app.base.models import Base
from app.database import async_session_factory
from app.logger import logger


class CrudMixin:
    model = Base

    @staticmethod
    async def _execute(query, commit: bool = False) -> Result[Any]:
        async with async_session_factory() as session:
            try:
                result = await session.execute(query)

                if commit:
                    await session.commit()
                return result

            except SQLAlchemyError as error:
                logger.error(f"Ошибка при работе с БД: {error}")
                await session.rollback()
                raise DataBaseError

    @classmethod
    async def _select_basic(cls, **kwargs) -> Result[Any]:
        query = select(cls.model.__table__.columns).filter_by(**kwargs)
        return await cls._execute(query)

    @classmethod
    async def _update_basic(
        cls, new_data: Mapping[str, Any], filter_by: Mapping[str, Any]
    ) -> Result[Any]:
        query = (update(cls.model).values(**new_data).filter_by(**filter_by)).returning(
            cls.model.__table__.columns
        )

        result = await cls._execute(query, commit=True)
        return result

    @classmethod
    async def _insert_basic(cls, **data) -> Result[Any]:
        query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
        result = await cls._execute(query, commit=True)
        return result


class BaseCRUD(CrudMixin):
    _SchemaType = TypeVar("_SchemaType", bound=pydantic.BaseModel)

    @classmethod
    async def select_by_id_or_none(cls, id: int) -> _SchemaType | None:
        result = await cls._select_basic(id=id)
        return result.mappings().one_or_none()

    @classmethod
    async def select_all(cls, **filter_by) -> list[_SchemaType]:
        result = await cls._select_basic(**filter_by)
        return result.mappings().all()  # noqa

    @classmethod
    async def update_by_id(cls, id: int, **new_data) -> _SchemaType:
        filter_by = {"id": id}
        result = await cls._update_basic(new_data, filter_by)

        return result.mappings().one()  # noqa

    @classmethod
    async def insert(cls, **data) -> _SchemaType:
        result = await cls._insert_basic(**data)
        return result.mappings().one()  # noqa
