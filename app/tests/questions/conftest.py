import faker
import pytest

from app.questions.crud import QuestionCRUD
from app.questions.enums import Levels, Status
from app.questions.models import Question


@pytest.fixture
async def create_question():
    fake = faker.Faker("ru_RU")

    async def question(
        save_in_db: bool = True,
        user_id: int = 1,
        title: str = fake.paragraph(nb_sentences=1),
        text: str = fake.paragraph(nb_sentences=2),
        answer: str = fake.paragraph(nb_sentences=1),
        level: Levels = Levels.junior,
        status: Status = Status.active,
        likes_count: int = 0,
        easy_count: int = 0,
        medium_count: int = 0,
        hard_count: int = 0,
        views_count: int = 0,
        got_at_interview: int = 0,
    ):
        if save_in_db:
            new_question = await QuestionCRUD.insert(
                user_id=user_id,
                title=title,
                text=text,
                answer=answer,
                level=level,
                status=status,
                likes_count=likes_count,
                easy_count=easy_count,
                medium_count=medium_count,
                hard_count=hard_count,
                views_count=views_count,
                got_at_interview=got_at_interview,
            )
        else:
            new_question = Question(
                user_id=user_id,
                title=title,
                text=text,
                answer=answer,
                level=level,
                status=status,
            )
        return new_question

    yield question


@pytest.fixture
async def create_list_with_questions(create_question):
    async def create_numbers_of_questions(number=10, save_db=False):
        lst = [await create_question(save_in_db=save_db) for _ in range(number)]

        return lst

    yield create_numbers_of_questions
