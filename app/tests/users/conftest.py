import pytest
import faker
from httpx import AsyncClient

from app.users.auth import get_password_hash
from app.users.crud import UserCRUD
from app.users.enums import Permission
from app.users.models import User


@pytest.fixture
async def create_user(session, async_client: AsyncClient):
    fake = faker.Faker('ru_RU')

    async def user(
        is_auth=False,
        email=fake.ascii_free_email(),
        password=fake.password(length=18),
        rights: Permission = Permission.user,
    ):
        if is_auth:
            response = await async_client.post('/auth/register', json={
                "email": email,
                "password": password,
                "rights": rights.value
            })

            response_json = response.json()
            id = response_json.get('id')
            rights = response_json.get('rights')

        else:
            hashed_password: str = await get_password_hash(password)
            user_data = await UserCRUD.insert(
                email=email, hashed_password=hashed_password, rights=rights
            )
            id = user_data.id
            rights = user_data.rights

        return User(id=id, email=email, rights=rights, hashed_password=password)

    yield user
