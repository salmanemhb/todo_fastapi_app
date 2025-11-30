"""
Unit tests for CRUD operations.
"""
import pytest
from app.crud import TaskRepository
from app.schemas import TaskCreate, TaskUpdate
from app.models import Task


class TestTaskRepository:
    """Test cases for TaskRepository class."""
    
    def test_create_task(self, db_session):
        """Test creating a new task."""
        task_data = TaskCreate(title="Test Task", description="Test Description")
        task = TaskRepository.create(db_session, task_data)
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
    
    def test_create_task_without_description(self, db_session):
        """Test creating a task without description."""
        task_data = TaskCreate(title="Test Task", description=None)
        task = TaskRepository.create(db_session, task_data)
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description is None
        assert task.completed is False
    
    def test_get_task_by_id(self, db_session):
        """Test retrieving a task by ID."""
        task_data = TaskCreate(title="Test Task", description="Test Description")
        created_task = TaskRepository.create(db_session, task_data)
        
        retrieved_task = TaskRepository.get_by_id(db_session, created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title
    
    def test_get_nonexistent_task(self, db_session):
        """Test retrieving a task that doesn't exist."""
        task = TaskRepository.get_by_id(db_session, 999)
        assert task is None
    
    def test_get_all_tasks(self, db_session):
        """Test retrieving all tasks."""
        # Create multiple tasks
        for i in range(5):
            task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
            TaskRepository.create(db_session, task_data)
        
        tasks = TaskRepository.get_all(db_session)
        assert len(tasks) == 5
    
    def test_get_all_tasks_with_pagination(self, db_session):
        """Test retrieving tasks with pagination."""
        # Create 10 tasks
        for i in range(10):
            task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
            TaskRepository.create(db_session, task_data)
        
        # Get first page
        page1 = TaskRepository.get_all(db_session, skip=0, limit=5)
        assert len(page1) == 5
        
        # Get second page
        page2 = TaskRepository.get_all(db_session, skip=5, limit=5)
        assert len(page2) == 5
        
        # Ensure no overlap
        assert page1[0].id != page2[0].id
    
    def test_update_task(self, db_session):
        """Test updating an existing task."""
        task_data = TaskCreate(title="Original Title", description="Original Description")
        task = TaskRepository.create(db_session, task_data)
        
        update_data = TaskUpdate(title="Updated Title", completed=True)
        updated_task = TaskRepository.update(db_session, task.id, update_data)
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"
        assert updated_task.completed is True
    
    def test_update_nonexistent_task(self, db_session):
        """Test updating a task that doesn't exist."""
        update_data = TaskUpdate(title="Updated Title")
        result = TaskRepository.update(db_session, 999, update_data)
        assert result is None
    
    def test_partial_update_task(self, db_session):
        """Test partial update of a task."""
        task_data = TaskCreate(title="Original Title", description="Original Description")
        task = TaskRepository.create(db_session, task_data)
        
        # Update only completed status
        update_data = TaskUpdate(completed=True)
        updated_task = TaskRepository.update(db_session, task.id, update_data)
        
        assert updated_task.title == "Original Title"
        assert updated_task.description == "Original Description"
        assert updated_task.completed is True
    
    def test_delete_task(self, db_session):
        """Test deleting a task."""
        task_data = TaskCreate(title="Test Task", description="Test Description")
        task = TaskRepository.create(db_session, task_data)
        task_id = task.id
        
        deleted_task = TaskRepository.delete(db_session, task_id)
        
        assert deleted_task.id == task_id
        assert TaskRepository.get_by_id(db_session, task_id) is None
    
    def test_delete_nonexistent_task(self, db_session):
        """Test deleting a task that doesn't exist."""
        result = TaskRepository.delete(db_session, 999)
        assert result is None
    
    def test_count_tasks(self, db_session):
        """Test counting tasks."""
        # Initially should be 0
        assert TaskRepository.count(db_session) == 0
        
        # Create 3 tasks
        for i in range(3):
            task_data = TaskCreate(title=f"Task {i}", description=f"Description {i}")
            TaskRepository.create(db_session, task_data)
        
        assert TaskRepository.count(db_session) == 3
    
    def test_task_to_dict(self, db_session):
        """Test task model to_dict method."""
        task_data = TaskCreate(title="Test Task", description="Test Description")
        task = TaskRepository.create(db_session, task_data)
        
        task_dict = task.to_dict()
        
        assert isinstance(task_dict, dict)
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] is False
        assert "id" in task_dict
