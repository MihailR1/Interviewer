from fastapi import APIRouter, Depends

from app.questions.crud import QuestionCRUD
from app.questions.exceptions import QuestionAlreadyExistError
from app.questions.models import Question
from app.questions.schemas import AddQuestion
from app.users.auth_utils import get_current_user
from app.users.models import User

router = APIRouter(prefix="/quenstions", tags=["Вопросы"])


@router.get("/all")
async def get_all_questions() -> list[Question]:
    result = await QuestionCRUD.select_all()

    return result


@router.post("/create")
async def create_question(
    question: AddQuestion, current_user: User = Depends(get_current_user)
) -> Question:

    exist_question = await QuestionCRUD.select_question_by_title_and_text(
        question.title, question.text)

    if exist_question:
        raise QuestionAlreadyExistError

    save = await QuestionCRUD.insert(user_id=current_user.id, **question.model_dump())

    return save
