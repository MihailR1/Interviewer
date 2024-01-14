import pytest
from fastapi import status
from httpx import AsyncClient

from app.questions.enums import Levels


@pytest.mark.parametrize(
    "is_auth_user, http_status",
    [(True, status.HTTP_200_OK), (False, status.HTTP_401_UNAUTHORIZED)],
)
async def test__create_question__auth_and_unauth_users(
    async_client: AsyncClient,
    create_question,
    create_user,
    is_auth_user,
    http_status,
):
    await create_user(is_auth=is_auth_user)
    question = await create_question(save_in_db=False)

    response = await async_client.post(
        "/questions/create",
        json={
            "title": question.title,
            "text": question.text,
            "answer": question.answer,
            "level": question.level.value,
        },
    )

    assert response.status_code == http_status


async def test__create_question__question_title_already_exist(
    async_client: AsyncClient, create_question, create_user
):
    title = "Чем отличается сравнение через == и is"

    await create_user(is_auth=True)
    await create_question(title=title, save_in_db=True)

    response = await async_client.post(
        "/questions/create",
        json={
            "title": title,
            "text": "Да ничем абсолютно точно",
            "answer": "Абсолютно ничем",
            "level": Levels.junior.value,
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
