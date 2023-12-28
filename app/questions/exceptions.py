from fastapi import status

from app.base.exceptions import BaseEx


class QuestionAlreadyExistError(BaseEx):
    status_code = status.HTTP_409_CONFLICT
    detail = "Вопрос уже есть в базе данных"
