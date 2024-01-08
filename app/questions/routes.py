import random

from fastapi import APIRouter, Depends

from app.questions.crud import QuestionCRUD
from app.questions.enums import StatsCount, Status
from app.questions.exceptions import QuestionAlreadyExistError
from app.questions.models import Question
from app.questions.schemas import AddQuestion
from app.users.auth_utils import get_current_user
from app.users.models import User

router = APIRouter(prefix="/quenstions", tags=["Вопросы"])


@router.get("/")
async def all_questions(number_of_questions: int = 15, is_random: bool = True) -> list[Question]:
    all_questions = await QuestionCRUD.select_questions_with_status(status=Status.active)

    if is_random:
        choice_random_questions = random.choices(all_questions, k=number_of_questions)
        return choice_random_questions

    return all_questions[:number_of_questions]


@router.post("/create")
async def create_question(
    question: AddQuestion, current_user: User = Depends(get_current_user)
) -> Question:
    exist_question = await QuestionCRUD.find_question_by_same_title_or_text(
        question.title, question.text
    )

    if exist_question:
        raise QuestionAlreadyExistError

    save = await QuestionCRUD.insert(user_id=current_user.id, **question.model_dump())

    return save


@router.get("/count_stats")
async def count_statistics_for_questions(question_id: int, stat_name: StatsCount) -> None:
    select_question = await QuestionCRUD.select_by_id_or_none(id=question_id)

    stat_value = getattr(select_question, stat_name.value)
    new_data = {stat_name.value: stat_value + 1}

    await QuestionCRUD.update_by_id(id=question_id, **new_data)
