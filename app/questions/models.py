from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.base.models import Base
from app.config import settings
from app.questions.enums import Levels, Status
from app.users.models import User


class CategoryQuestionLink(SQLModel, table=True):
    category_id: int | None = Field(
        default=None, foreign_key="Categories.id", primary_key=True
    )
    question_id: int | None = Field(
        default=None, foreign_key="Questions.id", primary_key=True
    )


class Category(Base, table=True):
    __tablename__ = "Categories"

    name: str = Field(default="Any", unique=True, description="Категории вопросов")
    questions: List["Question"] = Relationship(
        back_populates="categories", link_model=CategoryQuestionLink
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.name}"


class Question(Base, table=True):
    __tablename__ = "Questions"

    categories: List["Category"] | None = Relationship(
        back_populates="questions", link_model=CategoryQuestionLink
    )
    user_id: int = Field(default=None, foreign_key="Users.id")
    user: Optional["User"] = Relationship(back_populates="questions")
    title: str = Field(
        index=True,
        nullable=False,
        unique=True,
        min_length=settings.MIN_QUESTION_TITLE_TEXT_LENGTH,
        max_length=settings.MAX_QUESTION_TITLE_TEXT_LENGTH,
    )
    text: str = Field(
        nullable=False,
        unique=True,
        min_length=settings.MIN_QUESTION_TEXT_LENGTH,
        max_length=settings.MAX_QUESTION_TEXT_LENGTH,
    )
    answer: str = Field(nullable=False)
    level: Levels = Field(
        default=Levels.junior,
        description="Для какого уровня этот вопрос - Junior/Middle/Senior",
    )
    status: Status = Field(default=Status.moderation)
    likes_count: int = Field(default=0, description="Для подсчета кол-ва лайков")
    easy_count: int = Field(
        default=0,
        description="Для подсчета сколько людей посчитали вопрос простым/сложным",
    )
    middle_count: int = Field(default=0)
    hard_count: int = Field(default=0)
    got_at_interview: int = Field(
        default=0, description="Счетчик, скольким попадался на реальном собеседовании"
    )

    def __str__(self) -> str:
        return f"{self.id} - {self.title[:20]} - {self.text[:20]}"
