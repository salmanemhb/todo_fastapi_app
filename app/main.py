from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine, get_db
from app.models import Task
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate, Task as TaskSchema
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/tasks/", response_model=TaskSchema)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)

@app.get("/tasks/{task_id}", response_model=TaskSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/tasks/", response_model=List[TaskSchema])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@app.put("/tasks/{task_id}", response_model=TaskSchema)
def update_existing_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=TaskSchema)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/healthz")
def health():
    return {"status": "ok"}

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")