from typing import Dict, Any
from auth.jwt_handler import verify_token
from models import User
from sqlmodel import Session
from database_session import get_session
import uuid


def validate_and_get_user_from_token(token: str) -> Dict[str, Any]:
    """
    Validates a JWT token and extracts user information.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary containing user information
        
    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    # Verify the token and get payload
    payload = verify_token(token, "access")
    
    # Extract user_id from the payload
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise ValueError("Could not validate credentials - no user ID in token")
    
    # Convert user_id to UUID
    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise ValueError("Invalid user ID format in token")
    
    # Get user from database
    session_gen = get_session()
    session: Session = next(session_gen)
    try:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Return user information
        return {
            "id": user.id,
            "email": user.email
        }
    finally:
        session.close()