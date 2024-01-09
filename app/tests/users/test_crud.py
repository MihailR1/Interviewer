import pytest

from app.users.crud import UserCRUD


@pytest.mark.parametrize('email', ['teset@mail.ru', 'gmail@gmail.com', 'some@ria.ru'])
async def test__select_by_email_or_none__exist_user_by_email(create_user, email):
    user = await create_user(email=email, is_auth=False)
    select = await UserCRUD.select_by_email_or_none(user.email)

    assert select.email == user.email


@pytest.mark.parametrize('email', ['teset1@mail.ru', 'gmail3@gmail.com', 'some4@ria.ru'])
async def test__select_by_email_or_none__exist_user_by_id(create_user, email):
    user = await create_user(email=email, is_auth=False)
    select = await UserCRUD.select_by_email_or_none(user.email)

    assert select.id == user.id


async def test__select_by_email_or_none__user_not_exist():
    select = await UserCRUD.select_by_email_or_none('random@mail.ru')
    assert select is None
