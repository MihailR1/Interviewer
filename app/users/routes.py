from fastapi import APIRouter, Depends, Response

from app.users.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from app.users.crud import UserCRUD
from app.users.exceptions import UserAlreadyExistsException
from app.users.models import User
from app.users.schemas import UserAuth
from app.utils.cookie_enums import CookiesNames

router_users = APIRouter(prefix="/users", tags=["Пользователи"])
router_auth = APIRouter(prefix="/auth", tags=["Авторизация и регистрация"])


@router_auth.post("/register", status_code=201)
async def register_user(user_data: UserAuth) -> User:
    existing_user = await UserCRUD.find_by_email_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    new_user = await UserCRUD.insert(
        email=user_data.email, hashed_password=hashed_password
    )

    return new_user


@router_auth.post("/login")
async def login_user(response: Response, user_data: UserAuth) -> User:
    user = await authenticate_user(user_data.email, user_data.password)

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(CookiesNames.auth.value, access_token, httponly=True)

    return user


@router_auth.post("/logout")
async def logout_user(response: Response) -> bool:
    response.delete_cookie(CookiesNames.auth.value)
    return True


@router_users.get("/info")
async def user_info(current_user: User = Depends(get_current_user)) -> User:
    return current_user
