from datetime import datetime

from app.config import settings


def datetime_now() -> datetime:
    return datetime.now(settings.TIMEZONE)
