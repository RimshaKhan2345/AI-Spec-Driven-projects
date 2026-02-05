from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session
from models import User, UserCreate, UserRead
from utils.user_utils import create_user, get_user_by_email
from utils.password_utils import verify_password
from auth.jwt_handler import create_access_token, create_refresh_token, verify_token
from database_session import get_session
from datetime import timedelta
from config import settings

# Create a limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/register", response_model=UserRead)
@limiter.limit("100/hour")  # Increased for testing purposes
def register_user(request: Request, user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user with email and password.
    """
    # Check if user already exists
    existing_user = get_user_by_email(user.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = create_user(user, session)
    return db_user


@router.post("/login")
@limiter.limit("10/minute")
def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Authenticate user and return access and refresh tokens.
    """
    user = get_user_by_email(form_data.username, session)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
@limiter.limit("5/minute")
def refresh_token_endpoint(request: Request, refresh_token: str, session: Session = Depends(get_session)):
    """
    Generate a new access token using a refresh token.
    """
    payload = verify_token(refresh_token, token_type="refresh")
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify user still exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    new_access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }