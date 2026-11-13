from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.core.config import settings
from app.core.security import hash_password
from app.repositories.user_repo import UserRepository
from app.routes.public import auth as public_auth
from app.routes.admin import auth as admin_auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        if not repo.get_by_email(settings.ADMIN_EMAIL):
            repo.create_user(
                full_name="CodeEagle Admin",
                email=settings.ADMIN_EMAIL,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                role="admin",
            )
    finally:
        db.close()
    yield

app = FastAPI(title="CodeEagle Auth API", lifespan=lifespan)

app.include_router(public_auth.router, prefix="/api/v1")
app.include_router(admin_auth.router, prefix="/api/v1")