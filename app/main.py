import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.view import CategoryAdmin, QuestionsAdmin, UserAdmin
from app.config import settings
from app.database import engine
from app.questions.routes import router as questions_router
from app.users.routes import router_auth, router_users

if settings.MODE == 'PROD':
    sentry_sdk.init(dsn=settings.SENTRY_DSN, enable_tracing=True)

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
    allow_methods=["*"],
    allow_headers=["*"],
)
