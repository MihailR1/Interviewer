import pytest
import faker

from app.users.auth import get_password_hash
from app.users.crud import UserCRUD
from app.users.enums import Permission
from app.users.models import User


@pytest.fixture
async def create_user(session):
    fake = faker.Faker('ru_RU')

    async def user(
        email=fake.ascii_free_email(),
        password=fake.password(length=18),
        rights: Permission = Permission.user,
    ):
        hashed_password: str = await get_password_hash(password)
        new_user: User = await UserCRUD.insert(
            email=email, hashed_password=hashed_password, rights=rights
        )
        return new_user

    yield user
