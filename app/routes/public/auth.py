from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.schemas.auth import UserSignupRequest, UserResponse, TokenResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/public/auth", tags=["Public Portal - Auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def public_signup(payload: UserSignupRequest, db: Session = Depends(get_db)):
    return AuthService(db).register_public_user(payload)

@router.post("/login", response_model=TokenResponse)
def public_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService(db).authenticate_user(email=form_data.username, password=form_data.password)

@router.get("/me", response_model=UserResponse)
def get_public_profile(current_user: User = Depends(get_current_user)):
    return current_user