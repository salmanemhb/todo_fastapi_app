"""
Pydantic schemas for request/response validation.
Follows Interface Segregation Principle - different schemas for different use cases.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TaskBase(BaseModel):
    """Base schema with common task attributes."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating a task.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class Task(TaskBase):
    """Schema for task response with all fields including ID."""
    id: int
    completed: bool = False
    
    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    """Schema for health check endpoint response."""
    status: str
    database: str
    version: str