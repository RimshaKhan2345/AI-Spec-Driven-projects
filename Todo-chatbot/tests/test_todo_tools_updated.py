import pytest
from tools.todo_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    get_current_user_info
)
from models import User
from sqlmodel import Session
from database_session import get_session
import uuid
from auth.jwt_handler import create_access_token


def test_add_task():
    """Test adding a new task"""
    # Create a real user in the database first
    session: Session = next(get_session())
    try:
        # Create a new user
        user = User(
            email="test_add@example.com",
            password_hash="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Test adding a task
        result = add_task(
            user_id=str(user.id),
            title="Test Task",
            description="This is a test task"
        )
        
        # Verify the result
        assert result["success"] is True
        assert "Task 'Test Task' added successfully" in result["message"]
        assert "data" in result
        assert result["data"]["title"] == "Test Task"
        assert result["data"]["description"] == "This is a test task"
        
        # Clean up: delete the test task
        if "data" in result:
            task_id = result["data"]["id"]
            delete_result = delete_task(
                user_id=str(user.id),
                task_id=task_id
            )
            assert delete_result["success"] is True
        
        # Clean up: delete the user
        session.delete(user)
        session.commit()
    finally:
        session.close()


def test_list_tasks():
    """Test listing tasks"""
    # Create a real user in the database first
    session: Session = next(get_session())
    try:
        # Create a new user
        user = User(
            email="test_list@example.com",
            password_hash="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Add a test task first
        add_result = add_task(
            user_id=str(user.id),
            title="Test Task for Listing",
            description="This task will be listed"
        )
        assert add_result["success"] is True
        
        # Test listing tasks
        result = list_tasks(user_id=str(user.id))
        
        # Verify the result
        assert isinstance(result, list)
        assert len(result) >= 1
        assert any(task["title"] == "Test Task for Listing" for task in result)
        
        # Clean up: delete the test task
        if len(result) > 0:
            task_id = result[0]["id"]
            delete_result = delete_task(
                user_id=str(user.id),
                task_id=task_id
            )
            assert delete_result["success"] is True
        
        # Clean up: delete the user
        session.delete(user)
        session.commit()
    finally:
        session.close()


def test_complete_task():
    """Test completing a task"""
    # Create a real user in the database first
    session: Session = next(get_session())
    try:
        # Create a new user
        user = User(
            email="test_complete@example.com",
            password_hash="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Add a test task first
        add_result = add_task(
            user_id=str(user.id),
            title="Test Task for Completion",
            description="This task will be completed"
        )
        assert add_result["success"] is True
        task_id = add_result["data"]["id"]
        
        # Verify the task is initially not completed
        assert add_result["data"]["completed"] is False
        
        # Test completing the task
        result = complete_task(
            user_id=str(user.id),
            task_id=task_id
        )
        
        # Verify the result
        assert result["success"] is True
        assert "marked as completed" in result["message"]
        assert result["data"]["completed"] is True
        
        # Clean up: delete the test task
        delete_result = delete_task(
            user_id=str(user.id),
            task_id=task_id
        )
        assert delete_result["success"] is True
        
        # Clean up: delete the user
        session.delete(user)
        session.commit()
    finally:
        session.close()


def test_delete_task():
    """Test deleting a task"""
    # Create a real user in the database first
    session: Session = next(get_session())
    try:
        # Create a new user
        user = User(
            email="test_delete@example.com",
            password_hash="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Add a test task first
        add_result = add_task(
            user_id=str(user.id),
            title="Test Task for Deletion",
            description="This task will be deleted"
        )
        assert add_result["success"] is True
        task_id = add_result["data"]["id"]
        
        # Test deleting the task
        result = delete_task(
            user_id=str(user.id),
            task_id=task_id
        )
        
        # Verify the result
        assert result["success"] is True
        assert result["message"] == "Task deleted successfully"
        
        # Clean up: delete the user
        session.delete(user)
        session.commit()
    finally:
        session.close()


def test_update_task():
    """Test updating a task"""
    # Create a real user in the database first
    session: Session = next(get_session())
    try:
        # Create a new user
        user = User(
            email="test_update@example.com",
            password_hash="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Add a test task first
        add_result = add_task(
            user_id=str(user.id),
            title="Original Task Title",
            description="Original task description"
        )
        assert add_result["success"] is True
        task_id = add_result["data"]["id"]
        
        # Test updating the task
        result = update_task(
            user_id=str(user.id),
            task_id=task_id,
            title="Updated Task Title",
            description="Updated task description"
        )
        
        # Verify the result
        assert result["success"] is True
        assert "Task 'Updated Task Title' updated successfully" in result["message"]
        assert result["data"]["title"] == "Updated Task Title"
        assert result["data"]["description"] == "Updated task description"
        
        # Clean up: delete the test task
        delete_result = delete_task(
            user_id=str(user.id),
            task_id=task_id
        )
        assert delete_result["success"] is True
        
        # Clean up: delete the user
        session.delete(user)
        session.commit()
    finally:
        session.close()


def test_get_current_user_info():
    """Test getting current user info"""
    # Create a real user in the database first
    session: Session = next(get_session())
    try:
        # Create a new user
        user = User(
            email="test_info@example.com",
            password_hash="hashed_password_here"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Test getting user info
        result = get_current_user_info(user_id=str(user.id))
        
        # Verify the result
        assert result["success"] is True
        assert result["data"]["id"] == str(user.id)
        assert result["data"]["email"] == user.email
        
        # Clean up: delete the user
        session.delete(user)
        session.commit()
    finally:
        session.close()