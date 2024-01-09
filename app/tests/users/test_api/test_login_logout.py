from httpx import AsyncClient
from fastapi import status


async def test__login_user__correct_user_data(async_client: AsyncClient, create_user):
    user = await create_user()

    response = await async_client.post('/auth/login', json={
        'email': user.email,
        "password": user.hashed_password
    })

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get('auth_access_token') is not None


async def test__login_user__already_logged(async_client: AsyncClient, create_user):
    user = await create_user()
    await create_user(is_auth=True)

    response = await async_client.post('/auth/login', json={
        'email': user.email,
        "password": user.hashed_password
    })

    assert response.status_code == status.HTTP_200_OK


async def test__login_user__wrong_user_data(async_client: AsyncClient, create_user):
    response = await async_client.post('/auth/login', json={
        'email': '2323232@mail.ru',
        "password": '2312313'
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test__logout_user__correct_user_auth(async_client: AsyncClient, create_user):
    await create_user(is_auth=True)

    response = await async_client.post('/auth/logout')

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get('auth_access_token') is None


async def test__logout_user__user_unauth(async_client: AsyncClient):
    response = await async_client.post('/auth/logout')

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get('auth_access_token') is None


async def test__user_info__correct_logged_user(async_client: AsyncClient, create_user):
    user = await create_user(is_auth=True)

    response = await async_client.get('/users/info')
    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert result['email'] == user.email


async def test__user_info__user_not_auth(async_client: AsyncClient):
    response = await async_client.get('/users/info')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
