from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from database import get_session
from models.user import User
from utils import jwt_utils

router = APIRouter(tags=["authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    request: RegisterRequest,
    session: Session = Depends(get_session),
) -> UserResponse:
    existing_user = session.scalar(
        select(User).where(
            (User.username == request.username) | (User.email == request.email)
        )
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        )

    user = User(
        username=request.username,
        email=request.email,
        role=request.role,
        password_hash="",
    )
    user.set_password(request.password)
    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        ) from None

    session.refresh(user)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login_user(
    request: LoginRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:
    user = session.scalar(select(User).where(User.username == request.username))
    if user is None or not user.check_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(access_token=jwt_utils.create_token(user.id, user.role))
