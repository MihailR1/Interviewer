import enum
from datetime import datetime

from app.config import settings


def datetime_now() -> datetime:
    # return datetime.now(settings.TIMEZONE)
    return datetime.utcnow()


class CookiesNames(enum.Enum):
    auth = "auth_access_token"
