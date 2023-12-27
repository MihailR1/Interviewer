from fastapi import HTTPException, status

from app.base.exceptions import BaseEx


class WrongEmailOrPasswordException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class UserIsNotAuthException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не авторизован"


class UserAlreadyExistsException(BaseEx):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class TokenExpiredException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"
