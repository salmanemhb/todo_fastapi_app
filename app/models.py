"""
SQLAlchemy database models.
Follows Single Responsibility Principle - Task model only handles task data structure.
"""
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Task(Base):
    """
    Task model representing a TODO item.
    
    Attributes:
        id: Unique identifier for the task
        title: Task title (required)
        description: Detailed task description (optional)
        completed: Task completion status (default: False)
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        """String representation of the task."""
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
    
    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }