import pytest

from app.base.exceptions import DataBaseError
from app.users.auth import get_password_hash
from app.users.crud import UserCRUD


@pytest.mark.parametrize("email", ["teset@mail.ru", "gmail@gmail.com", "some@ria.ru"])
async def test__select_by_email_or_none__exist_user_by_email(create_user, email):
    user = await create_user(email=email, is_auth=False)
    select = await UserCRUD.select_by_email_or_none(user.email)

    assert select.email == user.email


@pytest.mark.parametrize(
    "email", ["teset1@mail.ru", "gmail3@gmail.com", "some4@ria.ru"]
)
async def test__select_by_id_or_none__exist_user_by_id(create_user, email):
    user = await create_user(email=email, is_auth=False)
    select = await UserCRUD.select_by_id_or_none(id=user.id)

    assert select.id == user.id


async def test__select_by_email_or_none__user_not_exist():
    select = await UserCRUD.select_by_email_or_none("random@mail.ru")
    assert select is None


@pytest.mark.parametrize(
    "email, password",
    [("emaill@email.ru", "28912738JKSHF871"), ("victor@gmail.com", "12356A")],
)
async def test__insert_user__new_user(email, password):
    hashed_password = await get_password_hash(password)

    user_data = await UserCRUD.insert(email=email, hashed_password=hashed_password)

    assert user_data.id is not None


async def test__insert_user_duplicate_email():
    email, password = "mihail@email.ru", "28912738JKSHF871"
    await UserCRUD.insert(email=email, hashed_password=password)

    with pytest.raises(DataBaseError):
        await UserCRUD.insert(email=email, hashed_password=password)
