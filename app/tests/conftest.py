import asyncio
import random

import faker
import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlmodel import SQLModel

from app.config import settings
from app.database import async_session_factory, engine
from app.main import app as fastapi_app
from app.questions.enums import Status
from app.questions.models import Question
from app.users.auth import get_password_hash
from app.users.crud import UserCRUD
from app.users.enums import Permission
from app.users.models import User


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    fake = faker.Faker("ru_RU")
    users = [
        {"email": fake.ascii_free_email(), "hashed_password": fake.password(length=18)}
        for _ in range(10)
    ]

    questions = [
        {
            "user_id": random.randint(1, 10),
            "title": fake.paragraph(nb_sentences=1),
            "text": fake.paragraph(nb_sentences=2),
            "answer": fake.paragraph(nb_sentences=1),
            "status": random.choice([Status.active, Status.moderation]),
        }
        for _ in range(10)
    ]

    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_factory() as session:
        await session.execute(insert(User).values(users))
        await session.flush()

        await session.execute(insert(Question).values(questions))
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def create_user(async_client: AsyncClient):
    fake = faker.Faker("ru_RU")

    async def user(
        is_auth=False,
        email=fake.ascii_free_email(),
        password=fake.password(length=18),
        rights: Permission = Permission.user,
    ):
        if is_auth:
            response = await async_client.post(
                "/auth/register",
                json={"email": email, "password": password, "rights": rights.value},
            )

            response_json = response.json()
            id = response_json.get("id")
            rights = response_json.get("rights")

        else:
            hashed_password: str = await get_password_hash(password)
            user_data = await UserCRUD.insert(
                email=email, hashed_password=hashed_password, rights=rights
            )
            id = user_data.id
            rights = user_data.rights

        return User(id=id, email=email, rights=rights, hashed_password=password)

    yield user
