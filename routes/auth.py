import jwt
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from core.dependencies import get_db
from models.user import User
from schemas.auth import LoginResponse, MessageResponse, RefreshResponse
from schemas.user import UserCreate, UserLogin, RegisterResponse, UserResponse
from services.auth import (
    create_user,
    authenticate_user,
    InvalidCredentials,
    create_refresh_token,
    refresh_tokens,
    logout_user,
)
from core.security import (
    create_access_token,
    get_current_user,
    get_admin_user,
)

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(data: UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:

    try:
        user = create_user(db, data.username, data.password)
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")

    return RegisterResponse(id=user.id, username=user.username)


@router.post("/login", response_model=LoginResponse)
def login(
    data: UserLogin, response: Response, db: Session = Depends(get_db)
) -> LoginResponse:
    try:
        user = authenticate_user(db, data.username, data.password)
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token: str = create_access_token(
        {"sub": str(user.id), "role": user.role.value}
    )

    refresh_token = create_refresh_token(user.id)

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token.token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return LoginResponse(
        access_token=access_token, user_id=user.id, username=user.username
    )


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse(id=user.id, username=user.username, role=user.role)


@router.get("/admin", response_model=MessageResponse)
def admin_panel(user: User = Depends(get_admin_user)) -> MessageResponse:
    return MessageResponse(message="welcome admin")


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token_route(
    request: Request, response: Response, db: Session = Depends(get_db)
) -> RefreshResponse:
    old_token: str | None = request.cookies.get("refresh_token")

    if not old_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    access, refresh = refresh_tokens(old_token, db)

    response.set_cookie(
        key="refresh_token", value=refresh, httponly=True, secure=False, samesite="lax"
    )

    return RefreshResponse(access_token=access)


@router.post("/logout", response_model=MessageResponse)
def logout(
    request: Request, response: Response, db: Session = Depends(get_db)
) -> MessageResponse:
    token_value: str | None = request.cookies.get("refresh_token")

    logout_user(token_value, db)

    response.delete_cookie(
        key="refresh_token", httponly=True, secure=True, samesite="lax"
    )

    return MessageResponse(message="logged out")
