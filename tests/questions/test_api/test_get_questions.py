import pytest
from fastapi import status
from httpx import AsyncClient

from app.questions.crud import QuestionCRUD


@pytest.mark.parametrize(
    "num_quest, is_random",
    [
        (15, True),
        (1, True),
        (230, True),
        (0, True),
        (0, False),
        (15, False),
        (2325, False),
    ],
)
async def test__all_questions(async_client: AsyncClient, num_quest, is_random):
    response = await async_client.get(
        "/questions/", params={"number_of_questions": num_quest, "is_random": is_random}
    )

    result = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(result) == num_quest if is_random or num_quest == 0 else len(result) >= 5


@pytest.mark.parametrize(
    "stat_name",
    [
        "easy_count",
        "medium_count",
        "hard_count",
        "got_at_interview",
        "views_count",
        "likes_count",
    ],
)
async def test__count_statistics_for_questions(async_client: AsyncClient, stat_name):
    question_id = 1
    response = await async_client.get(
        "/questions/count_stats",
        params={"question_id": question_id, "stat_name": stat_name},
    )

    assert response.status_code == status.HTTP_200_OK

    select_question = await QuestionCRUD.select_by_id_or_none(id=question_id)
    get_stats_value = getattr(select_question, stat_name)

    assert get_stats_value != 0
