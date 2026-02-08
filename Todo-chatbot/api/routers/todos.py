from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session
from typing import List
from models import Todo, TodoCreate, TodoUpdate, TodoRead, User
from database_session import get_session
from auth.jwt_handler import get_current_user
import uuid

# Create a limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


@router.post("/todos", response_model=TodoRead)
@limiter.limit("10/minute")
def create_todo(request: Request, todo: TodoCreate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=False,
        user_id=current_user.id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.get("/todos", response_model=List[TodoRead])
@limiter.limit("20/minute")
def read_todos(request: Request, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    todos = session.query(Todo).filter(Todo.user_id == current_user.id).all()
    return todos


@router.get("/todos/{todo_id}", response_model=TodoRead)
@limiter.limit("30/minute")
def read_todo(request: Request, todo_id: uuid.UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/todos/{todo_id}", response_model=TodoRead)
@limiter.limit("10/minute")
def update_todo(request: Request, todo_id: uuid.UUID, todo: TodoUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    db_todo = session.get(Todo, todo_id)
    if not db_todo or db_todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_data = todo.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.delete("/todos/{todo_id}")
@limiter.limit("10/minute")
def delete_todo(request: Request, todo_id: uuid.UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted successfully"}


@router.patch("/todos/{todo_id}/complete", response_model=TodoRead)
@limiter.limit("10/minute")
def toggle_todo_complete(request: Request, todo_id: uuid.UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    todo = session.get(Todo, todo_id)
    if not todo or todo.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.completed = not todo.completed
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo