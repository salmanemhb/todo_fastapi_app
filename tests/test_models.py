"""
Unit tests for database models.
"""
import pytest
from app.models import Task


class TestTaskModel:
    """Test cases for Task model."""
    
    def test_task_creation(self, db_session):
        """Test creating a task model."""
        task = Task(
            title="Test Task",
            description="Test Description",
            completed=False
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
    
    def test_task_repr(self, db_session):
        """Test task __repr__ method."""
        task = Task(title="Test Task", description="Test Description")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        repr_string = repr(task)
        assert "Task" in repr_string
        assert str(task.id) in repr_string
        assert "Test Task" in repr_string
    
    def test_task_to_dict(self, db_session):
        """Test task to_dict method."""
        task = Task(
            title="Test Task",
            description="Test Description",
            completed=True
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        task_dict = task.to_dict()
        
        assert isinstance(task_dict, dict)
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] is True
        assert task_dict["id"] == task.id
    
    def test_task_default_completed(self, db_session):
        """Test task completed field defaults to False."""
        task = Task(title="Test Task")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.completed is False
    
    def test_task_without_description(self, db_session):
        """Test creating a task without description."""
        task = Task(title="Test Task", description=None)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.description is None
