import enum


class Levels(enum.Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class Status(enum.Enum):
    active = "active"
    moderation = "moderation"


class StatsCount(enum.Enum):
    easy = "easy_count"
    medium = "medium_count"
    hard = "hard_count"
    got_at_interview = "got_at_interview"
    views = "views_count"
    likes = "likes_count"
