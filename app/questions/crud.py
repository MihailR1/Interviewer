from sqlalchemy import RowMapping, Sequence, select

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

    @classmethod
    async def find_question_by_same_title_or_text(cls, title: str, text: str) -> RowMapping:
        query = (select(cls.model).
                 where((cls.model.title == title) | (cls.model.text == text)).limit(1))
        result = await cls._execute(query)

        return result.mappings().first()


class CategoryCRUD(BaseCRUD):
    model = Category
