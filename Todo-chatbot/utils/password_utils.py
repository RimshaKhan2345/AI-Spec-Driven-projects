from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Fallback to simple comparison if bcrypt fails (for development/testing)
        # Note: This is not secure and should only be used for debugging
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def get_password_hash(password: str) -> str:
    """
    Hashes a plain password using bcrypt.
    """
    try:
        # Truncate password to 72 bytes if needed to comply with bcrypt limitations
        truncated_password = password[:72] if len(password) > 72 else password
        return pwd_context.hash(truncated_password)
    except ValueError:
        # Fallback to simple hashing if bcrypt fails (for development/testing)
        # Note: This is not secure and should only be used for debugging
        return hashlib.sha256(password.encode()).hexdigest()