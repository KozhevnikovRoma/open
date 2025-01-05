from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database.models.task import Task
from database.models.user import User
from database.database_manager import get_db_session

router = APIRouter()

# Pydantic-модели для валидации входных и выходных данных
class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

class ErrorResponse(BaseModel):
    detail: str

@router.post("/tasks/", response_model=TaskResponse, responses={
    400: {"model": ErrorResponse, "description": "Invalid data or user does not exist."},
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def create_task(task: TaskCreate, session: Session = Depends(get_db_session)):
    """
    Создание новой задачи.
    """
    try:
        # Проверяем существование пользователя
        user = session.query(User).filter(User.id == task.user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="User does not exist.")

        # Создаем задачу
        task_entry = Task(title=task.title, description=task.description, user_id=task.user_id)
        session.add(task_entry)
        session.commit()
        session.refresh(task_entry)

        return TaskResponse(
            id=task_entry.id,
            title=task_entry.title,
            description=task_entry.description,
            user_id=task_entry.user_id
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/tasks/{task_id}", response_model=TaskResponse, responses={
    404: {"model": ErrorResponse, "description": "Task not found."},
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def get_task(task_id: int, session: Session = Depends(get_db_session)):
    """
    Получение задачи по ID.
    """
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            user_id=task.user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/tasks/", response_model=List[TaskResponse], responses={
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def get_all_tasks(session: Session = Depends(get_db_session)):
    """
    Получение всех задач.
    """
    try:
        tasks = session.query(Task).all()
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                user_id=task.user_id
            ) for task in tasks
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.delete("/tasks/{task_id}", responses={
    204: {"description": "Task deleted successfully."},
    404: {"model": ErrorResponse, "description": "Task not found."},
    500: {"model": ErrorResponse, "description": "Internal server error."}
})
def delete_task(task_id: int, session: Session = Depends(get_db_session)):
    """
    Удаление задачи по ID.
    """
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")

        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error.")
