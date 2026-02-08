from typing import Dict, List, Optional
from sqlmodel import Session
from models import Todo, User, TodoCreate, TodoUpdate
from database_session import get_session
from utils.auth_wrapper import validate_and_get_user_from_token
import uuid


def add_task(user_id: str, title: str, description: str = None) -> Dict:
    """
    Creates a new todo for the specified user.

    Args:
        user_id: ID of the user creating the task
        title: Title of the task
        description: Optional description of the task

    Returns:
        Dictionary containing the created task information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return {"error": "Invalid user ID format"}

    # Create a new todo
    db_todo = Todo(
        title=title,
        description=description,
        completed=False,  # New tasks are not completed by default
        user_id=user_uuid
    )

    # Save to database
    session: Session = next(get_session())
    try:
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)

        return {
            "success": True,
            "message": f"Task '{db_todo.title}' added successfully",
            "data": {
                "id": str(db_todo.id),
                "title": db_todo.title,
                "description": db_todo.description,
                "completed": db_todo.completed,
                "user_id": str(db_todo.user_id),
                "created_at": db_todo.created_at.isoformat(),
                "updated_at": db_todo.updated_at.isoformat()
            }
        }
    except Exception as e:
        session.rollback()
        return {"success": False, "error": f"Failed to add task: {str(e)}"}
    finally:
        session.close()


def list_tasks(user_id: str, status: str = "all") -> List[Dict]:
    """
    Retrieves tasks for the specified user with optional filtering.

    Args:
        user_id: ID of the user whose tasks to retrieve
        status: Filter for task status ("all", "pending", "completed")

    Returns:
        List of dictionaries containing task information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return [{"success": False, "error": "Invalid user ID format"}]

    # Query tasks from database
    session: Session = next(get_session())
    try:
        query = session.query(Todo).filter(Todo.user_id == user_uuid)

        if status == "pending":
            query = query.filter(Todo.completed == False)
        elif status == "completed":
            query = query.filter(Todo.completed == True)
        # For "all", no additional filter is needed

        tasks = query.all()

        # Format the results
        result = []
        for task in tasks:
            result.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            })

        return result
    except Exception as e:
        return [{"success": False, "error": f"Failed to retrieve tasks: {str(e)}"}]
    finally:
        session.close()


def complete_task(user_id: str, task_id: str) -> Dict:
    """
    Marks a task as completed for the specified user.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to mark as completed

    Returns:
        Dictionary containing the updated task information
    """
    try:
        # Convert user_id and task_id to UUID
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return {"success": False, "error": "Invalid ID format"}

    # Find the task in the database
    session: Session = next(get_session())
    try:
        db_task = session.get(Todo, task_uuid)

        if not db_task:
            return {"success": False, "error": "Task not found"}

        if db_task.user_id != user_uuid:
            return {"success": False, "error": "Access denied: You can only complete your own tasks"}

        # Mark as completed
        db_task.completed = True
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "success": True,
            "message": f"Task '{db_task.title}' marked as completed",
            "data": {
                "id": str(db_task.id),
                "title": db_task.title,
                "description": db_task.description,
                "completed": db_task.completed,
                "user_id": str(db_task.user_id),
                "created_at": db_task.created_at.isoformat(),
                "updated_at": db_task.updated_at.isoformat()
            }
        }
    except Exception as e:
        session.rollback()
        return {"success": False, "error": f"Failed to complete task: {str(e)}"}
    finally:
        session.close()


def delete_task(user_id: str, task_id: str) -> Dict:
    """
    Deletes a task for the specified user.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to delete

    Returns:
        Dictionary containing success or error message
    """
    try:
        # Convert user_id and task_id to UUID
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return {"success": False, "error": "Invalid ID format"}

    # Find the task in the database
    session: Session = next(get_session())
    try:
        db_task = session.get(Todo, task_uuid)

        if not db_task:
            return {"success": False, "error": "Task not found"}

        if db_task.user_id != user_uuid:
            return {"success": False, "error": "Access denied: You can only delete your own tasks"}

        # Delete the task
        session.delete(db_task)
        session.commit()

        return {
            "success": True,
            "message": "Task deleted successfully"
        }
    except Exception as e:
        session.rollback()
        return {"success": False, "error": f"Failed to delete task: {str(e)}"}
    finally:
        session.close()


def update_task(user_id: str, task_id: str, title: str = None, description: str = None) -> Dict:
    """
    Updates an existing task for the specified user.

    Args:
        user_id: ID of the user who owns the task
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Dictionary containing the updated task information
    """
    try:
        # Convert user_id and task_id to UUID
        user_uuid = uuid.UUID(user_id)
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        return {"success": False, "error": "Invalid ID format"}

    # Find the task in the database
    session: Session = next(get_session())
    try:
        db_task = session.get(Todo, task_uuid)

        if not db_task:
            return {"success": False, "error": "Task not found"}

        if db_task.user_id != user_uuid:
            return {"success": False, "error": "Access denied: You can only update your own tasks"}

        # Prepare update data
        if title is not None:
            db_task.title = title
        if description is not None:
            db_task.description = description

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "success": True,
            "message": f"Task '{db_task.title}' updated successfully",
            "data": {
                "id": str(db_task.id),
                "title": db_task.title,
                "description": db_task.description,
                "completed": db_task.completed,
                "user_id": str(db_task.user_id),
                "created_at": db_task.created_at.isoformat(),
                "updated_at": db_task.updated_at.isoformat()
            }
        }
    except Exception as e:
        session.rollback()
        return {"success": False, "error": f"Failed to update task: {str(e)}"}
    finally:
        session.close()


def get_current_user_info(user_id: str) -> Dict:
    """
    Retrieves user information for the specified user.

    Args:
        user_id: ID of the user to retrieve information for

    Returns:
        Dictionary containing user information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return {"success": False, "error": "Invalid user ID format"}

    # Get user from database
    session: Session = next(get_session())
    try:
        user = session.get(User, user_uuid)

        if not user:
            return {"success": False, "error": "User not found"}

        return {
            "success": True,
            "data": {
                "id": str(user.id),
                "email": user.email
            }
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to retrieve user info: {str(e)}"}
    finally:
        session.close()