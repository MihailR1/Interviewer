from pydantic import BaseModel, EmailStr, Field

from app.config import settings
from app.questions.enums import Levels, Status


class AddQuestion(BaseModel):
    title: str = Field(min_length=settings.MIN_QUESTION_TITLE_TEXT_LENGTH,
                       max_length=settings.MAX_QUESTION_TITLE_TEXT_LENGTH)
    text: str = Field(min_length=settings.MIN_QUESTION_TEXT_LENGTH,
                      max_length=settings.MAX_QUESTION_TEXT_LENGTH)
    level: Levels = Field(default=Levels.junior)

