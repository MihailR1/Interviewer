from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.view import UserAdmin, QuestionsAdmin, QuestionsModerations
from app.config import settings
from app.database import engine
from app.questions.routes import router as questions_router
from app.admin.auth import authentication_backend
from app.users.routes import router_auth, router_users

app = FastAPI()
#authentication_backend=authentication_backend
admin = Admin(app, engine)

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(questions_router)

admin.add_view(UserAdmin)
admin.add_view(QuestionsAdmin)
admin.add_view(QuestionsModerations)


@app.on_event("startup")
async def startup() -> None:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
