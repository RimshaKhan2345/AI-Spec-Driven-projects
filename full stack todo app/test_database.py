from sqlmodel import Session
from database_session import get_session
from models import UserCreate
from utils.user_utils import create_user

def test_database_operations():
    # Create a test user
    user_create = UserCreate(email="test@example.com", password="password123")
    
    # Get a session
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Try to create the user
        result = create_user(user_create, session)
        print("User created successfully:", result.email)
    except Exception as e:
        print(f"User creation failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the session
        next(session_gen, None)  # This closes the session

if __name__ == "__main__":
    test_database_operations()