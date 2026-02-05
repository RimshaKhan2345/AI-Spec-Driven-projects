from sqlmodel import Session, select
from models import User, UserCreate
from utils.password_utils import get_password_hash


def create_user(user: UserCreate, session: Session) -> User:
    """
    Creates a new user with a hashed password.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(email: str, session: Session) -> User:
    """
    Retrieves a user by their email address.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user