import pytest

from app.base.exceptions import DataBaseError
from app.questions.crud import QuestionCRUD
from app.questions.models import Question
from app.questions.enums import Status


@pytest.mark.parametrize('status', [Status.active, Status.moderation])
async def test__select_questions_with_status__different_statuses(status):
    result = await QuestionCRUD.select_questions_with_status(status=status)

    assert len(result) is not None
    assert result[0].status == status


@pytest.mark.parametrize(
    'id, found_result',
    [
        (1, 1),
        (10, 1),
        (120, None),
        (310, None),
        (327812, None)
    ])
async def test__select_by_id_or_none__different_ids(id, found_result):
    result = await QuestionCRUD.select_by_id_or_none(id=id)
    assert result if found_result else result is None


async def test__insert_question__correct_question(create_question):
    question: Question = await create_question(save_in_db=False)

    new_question = await QuestionCRUD.insert(
        user_id=1,
        title=question.title,
        text=question.text,
        answer=question.answer
    )

    assert new_question.text == question.text


async def test__insert_question__question_title_already_exist(create_question):
    question: Question = await create_question(save_in_db=True)

    with pytest.raises(DataBaseError):
        await QuestionCRUD.insert(
            user_id=1,
            title=question.title,
            text=question.text,
            answer=question.answer
        )
