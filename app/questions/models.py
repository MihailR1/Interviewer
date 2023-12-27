from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship, SQLModel

from app.base.models import Base
from app.config import settings
from app.questions.enums import Levels
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

    name: str = Field(default="Any", description="Категории вопросов")
    questions: list["Question"] = Relationship(
        back_populates="categories", link_model=CategoryQuestionLink
    )


class Question(Base, table=True):
    __tablename__ = "Questions"

    user_id: int = ForeignKey("User.id")
    # user: "User" = relationship(back_populates='questions', lazy='joined')
    categories: list["Category"] = Relationship(
        back_populates="questions", link_model=CategoryQuestionLink
    )
    title: str = Field(
        index=True,
        nullable=False,
        min_length=settings.MIN_QUESTION_TITLE_TEXT_LENGTH,
        max_length=settings.MAX_QUESTION_TITLE_TEXT_LENGTH,
    )
    text: str = Field(
        nullable=False,
        min_length=settings.MIN_QUESTION_TEXT_LENGTH,
        max_length=settings.MAX_QUESTION_TEXT_LENGTH,
    )
    level: Levels = Field(
        default=Levels.junior,
        description="Для какого уровня этот вопрос - Junior/Middle/Senior",
    )
    likes_count: int | None = Field(default=0, description="Для подсчета кол-ва лайков")
    easy_count: int | None = Field(
        default=0,
        description="Для подсчета сколько людей посчитали вопрос простым/сложным",
    )
    middle_count: int | None = Field(default=0)
    hard_count: int | None = Field(default=0)
    got_at_interview: int | None = Field(
        default=0, description="Счетчик, скольким попадался на реальном собеседовании"
    )
