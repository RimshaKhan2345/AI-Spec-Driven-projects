import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.routers.auth.auth import register_user
from models import UserCreate
from database_session import get_session
from sqlmodel import Session

def test_registration():
    # Create a test user
    user_create = UserCreate(email="test@example.com", password="password123")
    
    # Get a session
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Call the register function directly
        result = register_user(None, user_create, session)
        print("Registration successful:", result)
    except Exception as e:
        print(f"Registration failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the session
        next(session_gen, None)  # This closes the session

if __name__ == "__main__":
    test_registration()