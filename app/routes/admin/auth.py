from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.core.permissions import require_admin
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/admin/auth", tags=["Admin Portal - Auth"])

@router.post("/login", response_model=TokenResponse)
def admin_login(payload: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).authenticate_user(
        email=payload.email,
        password=payload.password,
        required_role="admin",
    )

@router.get("/verify", response_model=UserResponse)
def verify_admin_session(admin_user: User = Depends(require_admin)):
    return admin_user