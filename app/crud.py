"""
CRUD operations for Task model.
Follows Single Responsibility Principle - each function has one clear purpose.
Follows Open/Closed Principle - easily extensible without modification.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas


class TaskRepository:
    """
    Repository pattern for Task operations.
    Provides abstraction over data access layer.
    """
    
    @staticmethod
    def create(db: Session, task: schemas.TaskCreate) -> models.Task:
        """
        Create a new task in the database.
        
        Args:
            db: Database session
            task: Task creation schema
            
        Returns:
            Created task model
        """
        db_task = models.Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_by_id(db: Session, task_id: int) -> Optional[models.Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            db: Database session
            task_id: ID of the task
            
        Returns:
            Task model if found, None otherwise
        """
        return db.query(models.Task).filter(models.Task.id == task_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Task]:
        """
        Retrieve all tasks with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of task models
        """
        return db.query(models.Task).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, task_id: int, task: schemas.TaskUpdate) -> Optional[models.Task]:
        """
        Update an existing task.
        
        Args:
            db: Database session
            task_id: ID of the task to update
            task: Task update schema
            
        Returns:
            Updated task model if found, None otherwise
        """
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task:
            update_data = task.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            db.commit()
            db.refresh(db_task)
        return db_task

    @staticmethod
    def delete(db: Session, task_id: int) -> Optional[models.Task]:
        """
        Delete a task from the database.
        
        Args:
            db: Database session
            task_id: ID of the task to delete
            
        Returns:
            Deleted task model if found, None otherwise
        """
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if db_task:
            db.delete(db_task)
            db.commit()
        return db_task
    
    @staticmethod
    def count(db: Session) -> int:
        """
        Count total number of tasks.
        
        Args:
            db: Database session
            
        Returns:
            Total count of tasks
        """
        return db.query(models.Task).count()


# Backward compatibility - maintain the same function signatures
def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    return TaskRepository.create(db, task)


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return TaskRepository.get_by_id(db, task_id)


def get_tasks(db: Session, skip: int = 0, limit: int = 10) -> List[models.Task]:
    return TaskRepository.get_all(db, skip, limit)


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate) -> Optional[models.Task]:
    return TaskRepository.update(db, task_id, task)


def delete_task(db: Session, task_id: int) -> Optional[models.Task]:
    return TaskRepository.delete(db, task_id)