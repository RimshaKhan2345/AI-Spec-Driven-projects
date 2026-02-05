from models import UserCreate

def test_email_validation():
    try:
        user = UserCreate(email="testuser123458@example.com", password="password123")
        print("User creation successful:", user.email)
    except Exception as e:
        print(f"User creation failed: {e}")

if __name__ == "__main__":
    test_email_validation()