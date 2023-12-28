from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.logger import logger
from app.users.auth import authenticate_user, create_access_token, get_current_user
from app.users.enums import Permission
from app.users.exceptions import (
    IncorrectTokenFormatException,
    TokenExpiredException,
    WrongEmailOrPasswordException,
)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        try:
            user = await authenticate_user(email, password)
        except WrongEmailOrPasswordException:
            return False

        if user and user.rights in (Permission.admin, Permission.moderator):
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"token": access_token})
        else:
            logger.info("Кто-то тестирует админку на прочность")
            return False

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            user = await get_current_user(token)
        except (TokenExpiredException, IncorrectTokenFormatException):
            return False

        if user:
            return True

        return False


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
