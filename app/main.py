from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.view import CategoryAdmin, QuestionsAdmin, UserAdmin
from app.config import settings
from app.database import engine
from app.questions.routes import router as questions_router
from app.users.routes import router_auth, router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(questions_router)

admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    templates_dir='app/admin/templates'
)
admin.add_view(QuestionsAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(UserAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup() -> None:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
