from pydantic import BaseModel, Field

from app.config import settings
from app.questions.enums import Levels


class AddQuestion(BaseModel):
    title: str = Field(
        min_length=settings.MIN_QUESTION_TITLE_TEXT_LENGTH,
        max_length=settings.MAX_QUESTION_TITLE_TEXT_LENGTH,
    )
    text: str = Field(
        min_length=settings.MIN_QUESTION_TEXT_LENGTH,
        max_length=settings.MAX_QUESTION_TEXT_LENGTH,
    )
    answer: str
    level: Levels = Field(default=Levels.junior)
