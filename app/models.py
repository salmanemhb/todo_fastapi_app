from sqlalchemy import Column, Integer, String
from app.database import Base
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Integer, default=0)  # 0 for False, 1 for True

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"