from sqlalchemy.orm import relationship
from sqlmodel import Field

from app.base.models import Base
from app.users.enums import Rights


class User(Base, table=True):
    __tablename__ = "Users"

    rights: Rights = Field(
        default=Rights.user, description="Права доступа: админ или обычный юзер"
    )
    email: str = Field(title="test@mail.ru", index=True)
    hashed_password: str = Field(nullable=False, exclude=True)
    username: str | None = Field(default=None, title="Username")
    # questions: list['Question'] | None = relationship(back_populates='user', lazy='joined')
