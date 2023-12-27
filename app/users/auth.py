from datetime import datetime, timedelta

from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.base.utils import CookiesNames
from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
    WrongEmailOrPasswordException,
)
from app.users.crud import UserCRUD
from app.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> User | None:
    user = await UserCRUD.find_by_email_or_none(email=email)

    if not user or (user and not verify_password(password, user.hashed_password)):
        raise WrongEmailOrPasswordException

    return user


def get_token(request: Request) -> str:
    token = request.cookies.get(CookiesNames.auth.value)

    if not token:
        raise TokenAbsentException

    return token


async def get_current_user(token: str = Depends(get_token)) -> User | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException

    user_id: str = payload.get("sub")

    if not user_id:
        raise UserIsNotPresentException

    user = await UserCRUD.find_by_id_or_none(id=int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user
