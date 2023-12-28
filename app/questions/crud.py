from sqlalchemy import RowMapping, Sequence

from app.base.crud import BaseCRUD
from app.questions.enums import Status
from app.questions.models import Category, Question


class QuestionCRUD(BaseCRUD):
    model = Question

    @classmethod
    async def select_questions_with_status(
        cls, status: Status = Status.active
    ) -> Sequence[RowMapping]:
        result = await cls._select_basic(status=status)
        return result.mappings().all()


class CategoryCRUD(BaseCRUD):
    model = Category
