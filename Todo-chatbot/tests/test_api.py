import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import create_engine, SQLModel
from sqlmodel.pool import StaticPool
from database import engine
from unittest.mock import patch


# Create a test client with an in-memory database
@pytest.fixture(scope="module")
def test_client():
    # Use an in-memory SQLite database for testing
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Override the database engine in the app
    with patch('database.engine', test_engine):
        # Create all tables
        SQLModel.metadata.create_all(bind=test_engine)
        
        with TestClient(app) as client:
            yield client


def test_read_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}


def test_register_user(test_client):
    # Test user registration
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    response = test_client.post("/api/register", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "id" in data
    assert data["email"] == user_data["email"]