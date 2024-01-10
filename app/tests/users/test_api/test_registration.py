import pytest
from fastapi import status
from httpx import AsyncClient

from app.users.crud import UserCRUD


@pytest.mark.parametrize(
    "email, password, http_status",
    [
        ("User@yandex.ru", "2781KJSfh19!_f90128sdf", status.HTTP_201_CREATED),
        ("jackstone@gmail.com", "123452a", status.HTTP_201_CREATED),
        ("ussseeer@mail.ru", "123456", status.HTTP_201_CREATED),
        ("ussseeer@mail.ru", "123456", status.HTTP_409_CONFLICT),
        ("hello@example,com", "1234", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("check@gmail.com", "Nnn", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("test@mail.ru", "Non1", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("hello@hello", "@#!@2312312", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("@hello.ru", "2198271KJHSF", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("hello.ru", "12345", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test__register_user__different_situations(
    async_client: AsyncClient, email, password, http_status
):
    response = await async_client.post(
        "/auth/register", json={"email": email, "password": password}
    )

    assert response.status_code == http_status


async def test__register_user__check_password_in_db_is_hashed(
    async_client: AsyncClient, create_user
):
    password = "32489FKj123"
    email = "some@example.com"

    response = await async_client.post(
        "/auth/register", json={"email": email, "password": password}
    )

    select_user = await UserCRUD.select_by_email_or_none(email=email)

    assert response.status_code == status.HTTP_201_CREATED
    assert password != select_user.hashed_password


async def test__register_user__auth_cookie_set_correctly(async_client: AsyncClient):
    assert async_client.cookies.get("auth_access_token") is None

    response = await async_client.post(
        "/auth/register",
        json={"email": "randomaemail@yahoo.com", "password": "238923jkhfs"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert async_client.cookies.get("auth_access_token") is not None
