from fastapi import HTTPException, status


class BaseEx(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class DataBaseError(BaseEx):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка при обращении к базе данных"


class ValidationSchemaError(BaseEx):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка валидации данных"


class WrongEmailOrPasswordException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BaseEx):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не авторизован"


class UserAlreadyExistsException(BaseEx):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"
