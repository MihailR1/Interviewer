from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    __tablename__ = "base"

    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    created: datetime = Field(
        default=datetime.utcnow,
        sa_column_kwargs={"server_default": text("TIMEZONE('utc', now())")}
    )
    updated: datetime = Field(
        default=datetime.utcnow,
        sa_column_kwargs={
            "server_default": text("TIMEZONE('utc', now())"),
            "onupdate": text("TIMEZONE('utc', now())"),
        }
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.id}"
