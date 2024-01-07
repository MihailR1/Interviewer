from sqlalchemy import select

from app.base.crud import BaseCRUD
from app.questions.enums import Status
from app.questions.models import Category, Question


class QuestionCRUD(BaseCRUD):
    model = Question

    @classmethod
    async def select_questions_with_status(
        cls, status: Status = Status.active
    ) -> list[BaseCRUD._SchemaType]:
        result = await cls._select_basic(status=status)
        return result.mappings().all()  # noqa

    @classmethod
    async def find_question_by_same_title_or_text(
        cls, title: str, text: str
    ) -> BaseCRUD._SchemaType:
        query = (
            select(cls.model)
            .where((cls.model.title == title) | (cls.model.text == text))
            .limit(1)
        )
        result = await cls._execute(query)

        return result.mappings().first()


class CategoryCRUD(BaseCRUD):
    model = Category
