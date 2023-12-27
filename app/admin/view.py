from sqladmin import Admin, ModelView

from app.questions.models import Question
from app.users.models import User
from app.questions.enums import Status


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username, User.created]
    column_searchable_list = [User.email, User.username]
    column_sortable_list = [User.created, User.id]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True


class QuestionsAdmin(ModelView, model=Question):
    column_list = [Question.id, Question.status, Question.title, Question.text, Question.level, Question.updated]
    column_searchable_list = [Question.title, Question.text]
    column_sortable_list = [Question.status, Question.updated, Question.id, Question.level]
    name = "Question"
    name_plural = "Question"
    icon = "fa-solid fa-book"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class QuestionsModerations(ModelView, model=Question):
    column_list = [c.name for c in Question.__table__.c]
    column_searchable_list = [Question.title, Question.text]
    column_sortable_list = [Question.status, Question.updated, Question.id, Question.level]
    name = "Question Moderation"
    name_plural = "Questions Moderation"
    icon = "fa-solid fa-book"
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
