"""
Unit tests for Pydantic schemas.
"""
import pytest
from pydantic import ValidationError
from app.schemas import TaskBase, TaskCreate, TaskUpdate, Task, HealthResponse


class TestTaskSchemas:
    """Test cases for Task schemas."""
    
    def test_task_base_valid(self):
        """Test TaskBase with valid data."""
        task = TaskBase(title="Test Task", description="Test Description")
        assert task.title == "Test Task"
        assert task.description == "Test Description"
    
    def test_task_base_without_description(self):
        """Test TaskBase without description."""
        task = TaskBase(title="Test Task")
        assert task.title == "Test Task"
        assert task.description is None
    
    def test_task_base_empty_title(self):
        """Test TaskBase with empty title should fail."""
        with pytest.raises(ValidationError):
            TaskBase(title="", description="Test")
    
    def test_task_base_title_too_long(self):
        """Test TaskBase with title exceeding max length."""
        long_title = "A" * 201
        with pytest.raises(ValidationError):
            TaskBase(title=long_title)
    
    def test_task_create_valid(self):
        """Test TaskCreate schema."""
        task = TaskCreate(title="New Task", description="New Description")
        assert task.title == "New Task"
        assert task.description == "New Description"
    
    def test_task_update_partial(self):
        """Test TaskUpdate with partial data."""
        # Update only title
        task_update = TaskUpdate(title="Updated Title")
        assert task_update.title == "Updated Title"
        assert task_update.description is None
        assert task_update.completed is None
        
        # Update only completed
        task_update2 = TaskUpdate(completed=True)
        assert task_update2.title is None
        assert task_update2.completed is True
    
    def test_task_update_all_fields(self):
        """Test TaskUpdate with all fields."""
        task_update = TaskUpdate(
            title="Updated Title",
            description="Updated Description",
            completed=True
        )
        assert task_update.title == "Updated Title"
        assert task_update.description == "Updated Description"
        assert task_update.completed is True
    
    def test_task_schema_valid(self):
        """Test Task response schema."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False
        )
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
    
    def test_task_schema_default_completed(self):
        """Test Task schema with default completed value."""
        task = Task(id=1, title="Test Task", description="Test Description")
        assert task.completed is False


class TestHealthResponse:
    """Test cases for HealthResponse schema."""
    
    def test_health_response_valid(self):
        """Test HealthResponse with valid data."""
        health = HealthResponse(
            status="healthy",
            database="healthy",
            version="2.0.0"
        )
        assert health.status == "healthy"
        assert health.database == "healthy"
        assert health.version == "2.0.0"
    
    def test_health_response_degraded(self):
        """Test HealthResponse with degraded status."""
        health = HealthResponse(
            status="degraded",
            database="unhealthy",
            version="2.0.0"
        )
        assert health.status == "degraded"
        assert health.database == "unhealthy"
