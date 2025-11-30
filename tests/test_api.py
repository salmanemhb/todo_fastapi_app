"""
Integration tests for API endpoints.
"""
import pytest
from fastapi import status


class TestHealthEndpoints:
    """Test cases for health check endpoints."""
    
    def test_health_endpoint(self, client):
        """Test /health endpoint returns correct status."""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "version" in data
        assert data["version"] == "2.0.0"
    
    def test_healthz_endpoint(self, client):
        """Test /healthz endpoint for Kubernetes."""
        response = client.get("/healthz")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "ok"


class TestTaskEndpoints:
    """Test cases for task CRUD endpoints."""
    
    def test_create_task(self, client, sample_task):
        """Test creating a new task via API."""
        response = client.post("/tasks/", json=sample_task)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_task["title"]
        assert data["description"] == sample_task["description"]
        assert data["completed"] is False
        assert "id" in data
    
    def test_create_task_without_description(self, client):
        """Test creating a task without description."""
        task_data = {"title": "Task without description"}
        response = client.post("/tasks/", json=task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Task without description"
        assert data["description"] is None
    
    def test_create_task_invalid_data(self, client):
        """Test creating a task with invalid data."""
        # Missing required title field
        response = client.post("/tasks/", json={"description": "No title"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_get_task(self, client, sample_task):
        """Test retrieving a specific task."""
        # Create a task first
        create_response = client.post("/tasks/", json=sample_task)
        task_id = create_response.json()["id"]
        
        # Retrieve the task
        response = client.get(f"/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == sample_task["title"]
    
    def test_get_nonexistent_task(self, client):
        """Test retrieving a task that doesn't exist."""
        response = client.get("/tasks/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_all_tasks(self, client, sample_tasks):
        """Test retrieving all tasks."""
        # Create multiple tasks
        for task in sample_tasks:
            client.post("/tasks/", json=task)
        
        # Get all tasks
        response = client.get("/tasks/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == len(sample_tasks)
    
    def test_get_tasks_with_pagination(self, client, sample_tasks):
        """Test retrieving tasks with pagination."""
        # Create tasks
        for task in sample_tasks:
            client.post("/tasks/", json=task)
        
        # Get with limit
        response = client.get("/tasks/?skip=0&limit=2")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
    
    def test_update_task(self, client, sample_task):
        """Test updating a task."""
        # Create a task
        create_response = client.post("/tasks/", json=sample_task)
        task_id = create_response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Title",
            "completed": True
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["completed"] is True
    
    def test_update_nonexistent_task(self, client):
        """Test updating a task that doesn't exist."""
        update_data = {"title": "Updated Title"}
        response = client.put("/tasks/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_partial_update_task(self, client, sample_task):
        """Test partial update of a task."""
        # Create a task
        create_response = client.post("/tasks/", json=sample_task)
        task_id = create_response.json()["id"]
        
        # Partially update (only completed field)
        update_data = {"completed": True}
        response = client.put(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == sample_task["title"]  # Title unchanged
        assert data["completed"] is True  # Completed updated
    
    def test_delete_task(self, client, sample_task):
        """Test deleting a task."""
        # Create a task
        create_response = client.post("/tasks/", json=sample_task)
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == task_id
        
        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist."""
        response = client.delete("/tasks/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestStatisticsEndpoint:
    """Test cases for statistics endpoint."""
    
    def test_task_statistics(self, client, sample_tasks):
        """Test retrieving task statistics."""
        # Create tasks
        for task in sample_tasks:
            client.post("/tasks/", json=task)
        
        # Mark one as completed
        client.put("/tasks/1", json={"completed": True})
        
        # Get statistics
        response = client.get("/tasks/stats/summary")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 3
        assert data["completed"] == 1
        assert data["pending"] == 2
    
    def test_statistics_empty_database(self, client):
        """Test statistics with no tasks."""
        response = client.get("/tasks/stats/summary")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert data["completed"] == 0
        assert data["pending"] == 0


class TestRootEndpoint:
    """Test cases for root endpoint."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint serves HTML."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
