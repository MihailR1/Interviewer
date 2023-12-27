from app.base.crud import BaseCRUD
from app.questions.models import Category, Question


class QuestionCRUD(BaseCRUD):
    model = Question


class CategoryCRUD(BaseCRUD):
    model = Category
