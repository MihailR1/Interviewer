from fastapi import Depends, Request, Response
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import EmailStr

from app.config import settings
from app.users.auth import create_access_token, verify_password
from app.users.crud import UserCRUD
from app.users.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotAuthException,
    WrongEmailOrPasswordException,
)
from app.users.models import User
from app.utils.cookie_enums import CookiesNames


async def get_token(request: Request) -> str:
    token = request.cookies.get(CookiesNames.auth.value)

    if not token:
        raise TokenAbsentException

    return token


async def authenticate_user(email: EmailStr, password: str) -> User:
    user = await UserCRUD.select_by_email_or_none(email=email)

    if not user or (user and not await verify_password(password, user.hashed_password)):
        raise WrongEmailOrPasswordException

    return user


async def get_current_user(token: str = Depends(get_token)) -> User | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    user_id: str = payload.get(CookiesNames.auth.name)

    if not user_id:
        raise UserIsNotAuthException

    user = await UserCRUD.select_by_id_or_none(id=int(user_id))

    if not user:
        raise UserIsNotAuthException

    return user


async def create_and_set_access_token_for_login(
    response: Response, user_id: int
) -> None:
    data_for_token = {CookiesNames.auth.name: str(user_id)}

    access_token = await create_access_token(data_for_token)
    response.set_cookie(CookiesNames.auth.value, access_token, httponly=True)
