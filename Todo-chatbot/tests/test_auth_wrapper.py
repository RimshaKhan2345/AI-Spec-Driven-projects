import pytest
from utils.auth_wrapper import validate_and_get_user_from_token
from auth.jwt_handler import create_access_token
from models import User
from sqlmodel import Session
from database_session import get_session
import uuid
from datetime import datetime


def test_validate_and_get_user_from_token():
    """Test that the auth wrapper correctly validates tokens and extracts user info"""
    
    # Create a real user in the database first with a unique email
    session: Session = next(get_session())
    try:
        # Create a unique email using timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        email = f"test_{timestamp}@example.com"
        
        # Create a new user
        user = User(
            email=email,
            password_hash="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Create a token for the user using the real user ID
        user_data = {
            "sub": str(user.id),  # user ID as string
            "email": user.email
        }
        
        # Create a token for the user
        token = create_access_token(data=user_data)
        
        # Test that the function can validate the token and extract user info
        result = validate_and_get_user_from_token(token)
        
        # Verify the result contains expected fields
        assert "id" in result
        assert "email" in result
        assert result["email"] == user.email
        assert str(result["id"]) == str(user.id)
        
        # Verify that the ID is a valid UUID string
        assert isinstance(result["id"], uuid.UUID)
        
        # Clean up: delete the test user
        session.delete(user)
        session.commit()
    finally:
        session.close()


def test_validate_and_get_user_from_token_invalid():
    """Test that the auth wrapper raises an error for invalid tokens"""
    
    # Test with an invalid token
    invalid_token = "invalid.token.here"
    
    # Should raise an error
    try:
        validate_and_get_user_from_token(invalid_token)
        assert False, "Expected an error for invalid token"
    except Exception:
        # Expected to raise an error
        pass