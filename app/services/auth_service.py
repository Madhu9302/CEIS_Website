from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserSignupRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_public_user(self, payload: UserSignupRequest):
        if self.user_repo.get_by_email(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        return self.user_repo.create_user(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            role="user",
        )

    def authenticate_user(self, email: str, password: str, required_role: str | None = None) -> TokenResponse:
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if required_role and user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: {required_role} portal privileges required",
            )

        token = create_access_token(data={"sub": user.email, "role": user.role})
        return TokenResponse(access_token=token, role=user.role)