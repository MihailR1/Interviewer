from fastapi import APIRouter, Depends, Response

from app.users.auth import get_password_hash
from app.users.auth_utils import (
    authenticate_user,
    create_and_set_access_token_for_login,
    get_current_user,
)
from app.users.crud import UserCRUD
from app.users.exceptions import UserAlreadyExistsException
from app.users.models import User
from app.users.schemas import UserAuth
from app.utils.cookie_enums import CookiesNames

router_users = APIRouter(prefix="/users", tags=["Пользователи"])
router_auth = APIRouter(prefix="/auth", tags=["Авторизация и регистрация"])


@router_auth.post("/register", status_code=201)
async def register_user(response: Response, user_data: UserAuth) -> User:
    existing_user = await UserCRUD.select_by_email_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = await get_password_hash(user_data.password)
    new_user = await UserCRUD.insert(
        email=user_data.email, hashed_password=hashed_password
    )
    await create_and_set_access_token_for_login(response, new_user.id)

    return new_user


@router_auth.post("/login")
async def login_user(response: Response, user_data: UserAuth) -> User:
    user = await authenticate_user(user_data.email, user_data.password)
    await create_and_set_access_token_for_login(response, user.id)

    return user


@router_auth.post("/logout")
async def logout_user(response: Response) -> bool:
    response.delete_cookie(CookiesNames.auth.value)
    return True


@router_users.get("/info")
async def user_info(current_user: User = Depends(get_current_user)) -> User:
    return current_user
