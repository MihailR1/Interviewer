from datetime import datetime

from sqlmodel import Field, SQLModel

from app.utils.date_time import datetime_now


class Base(SQLModel):
    __tablename__ = "base"

    id: int = Field(default=None, nullable=False, primary_key=True, index=True)
    created: datetime = Field(default_factory=datetime_now)
    updated: datetime = Field(default_factory=datetime_now)
