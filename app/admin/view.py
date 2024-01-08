from sqladmin import ModelView

from app.questions.models import Category, Question
from app.users.models import User


class QuestionsAdmin(ModelView, model=Question):
    column_list = [
        Question.id,
        Question.status,
        Question.title,
        Question.text,
        Question.level,
        Question.updated,
    ]
    column_formatters = {Question.title: lambda m, a: m.title[:80],
                         Question.text: lambda m, a: m.text[:120]}
    column_searchable_list = [Question.title, Question.text]
    column_sortable_list = [
        Question.status,
        Question.updated,
        Question.id,
        Question.level,
    ]
    edit_template = "custom_edit.html"
    name = "Question"
    name_plural = "Questions"
    icon = "fa-solid fa-book"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    # def list_query(self, request: Request) -> Select:
    #     return select(self.model).where(self.model.status == Status.moderation)


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.name, Category.questions, Category.updated]
    column_searchable_list = [Category.name, Category.questions]
    column_sortable_list = [
        Category.id,
        Category.questions,
        Question.updated,
        Category.name,
    ]
    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-book"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.rights, User.email, User.username, User.created]
    column_searchable_list = [User.email, User.username]
    column_sortable_list = [User.rights, User.created, User.id]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True
