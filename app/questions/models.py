from typing import List, Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT
from sqlmodel import Field, Relationship, SQLModel

from app.base.models import Base
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
    title: str = Field(sa_column=Column(TEXT, index=True, nullable=False, unique=True))
    text: str = Field(sa_column=Column(TEXT, index=True, nullable=False))
    answer: str = Field(sa_column=Column(TEXT, index=True, nullable=False))
    level: Levels = Field(default=Levels.junior)
    status: Status = Field(default=Status.moderation)
    likes_count: int = Field(default=0, description="Для подсчета кол-ва лайков")
    easy_count: int = Field(
        default=0,
        description="Для подсчета сколько людей посчитали вопрос простым/сложным",
    )
    medium_count: int = Field(default=0)
    hard_count: int = Field(default=0)
    views_count: int = Field(default=0)
    got_at_interview: int = Field(default=0)

    def __str__(self) -> str:
        return f"{self.id} - {self.title[:20]} - {self.text[:20]}"
