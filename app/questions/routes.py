from fastapi import APIRouter

from app.questions.crud import QuestionCRUD
from app.questions.models import Question

router = APIRouter(prefix="/user", tags=["Вопросы"])


@router.get("/all")
async def get_all_questions() -> list[Question]:
    result = await QuestionCRUD.select_all()

    return result
