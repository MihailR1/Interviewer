from httpx import AsyncClient
from fastapi import status


async def test__register_user__register_new_user(async_client: AsyncClient):
    response = await async_client.post('/auth/register', json={
        "email": "test@example.com",
        "password": "3872Shfas"
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.cookies.get('auth_access_token') is not None


async def test__register_user__try_register_existing_user(async_client: AsyncClient, create_user):
    user = await create_user()

    response = await async_client.post('/auth/register', json={
        "email": user.email,
        "password": 'password21312'
    })

    assert response.status_code == status.HTTP_409_CONFLICT
