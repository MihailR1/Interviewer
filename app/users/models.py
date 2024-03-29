from typing import Optional

from sqlmodel import Field, Relationship

from app.base.models import Base
from app.users.enums import Permission


class User(Base, table=True):
    __tablename__ = "Users"

    rights: Permission = Field(
        default=Permission.user, description="Права доступа: админ или обычный юзер"
    )
    email: str = Field(
        index=True,
        unique=True,
        title="test@mail.ru",
    )
    hashed_password: str = Field(nullable=False, exclude=True)
    username: str | None = Field(default=None, unique=True, title="Username")
    questions: Optional["Question"] = Relationship(back_populates="user")

    def __str__(self) -> str:
        return f"{self.rights.value} - {self.email}"
