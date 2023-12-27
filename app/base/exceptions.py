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
