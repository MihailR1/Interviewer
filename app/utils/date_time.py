from datetime import datetime


def datetime_now() -> datetime:
    # return datetime.now(settings.TIMEZONE)
    return datetime.utcnow()
