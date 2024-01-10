import pytest
from httpx import AsyncClient
from fastapi import status

from app.users.crud import UserCRUD


@pytest.mark.parametrize(
    'email, password',
    [
        ('User@yandex.ru', '2781KJSfh19!_f90128sdf'),
        ('jackstone@gmail.com', '123452a'),
        ('ussseeer@mail.ru', '123456')
    ]
)
async def test__register_user__correct_new_user(async_client: AsyncClient, email, password):
    response = await async_client.post('/auth/register', json={
        "email": email,
        "password": password
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.cookies.get('auth_access_token') is not None


@pytest.mark.parametrize(
    'email, password',
    [
        ('hello@example,com', '1234'),
        ('check@gmail.com', 'Nnn'),
        ('test@mail.ru', 'Non1'),
        ('hello@hello', '@#!@2312312'),
        ('@hello.ru', '2198271KJHSF'),
        ('hello.ru', '12345')

    ])
async def test__register_user__not_valid_email_or_password(
    async_client: AsyncClient, email, password
):
    response = await async_client.post('/auth/register', json={
        "email": email,
        "password": password
    })

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test__register_user__check_password_in_db_is_hashed(async_client: AsyncClient,
                                                              create_user):
    password = '32489FKj123'
    email = 'some@example.com'

    response = await async_client.post('/auth/register', json={
        "email": email,
        "password": password
    })

    select_user = await UserCRUD.select_by_email_or_none(email=email)

    assert response.status_code == status.HTTP_201_CREATED
    assert password != select_user.hashed_password


async def test__register_user__email_already_in_database(async_client: AsyncClient, create_user):
    user = await create_user()

    response = await async_client.post('/auth/register', json={
        "email": user.email,
        "password": 'password21312'
    })

    assert response.status_code == status.HTTP_409_CONFLICT
