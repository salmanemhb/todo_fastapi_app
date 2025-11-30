"""
Main FastAPI application module.
Implements REST API for TODO task management with monitoring and health checks.
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import time

from app.config import get_settings
from app.database import Base, engine, get_db, check_db_connection
from app.models import Task
from app.crud import create_task, get_task, get_tasks, update_task, delete_task, TaskRepository
from app.schemas import TaskCreate, TaskUpdate, Task as TaskSchema, HealthResponse

# Get application settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A modern TODO application with FastAPI, featuring monitoring and DevOps best practices",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Setup Prometheus metrics
try:
    from app.monitoring import setup_metrics, track_task_operation, update_task_gauges
    instrumentator = setup_metrics(app)
    if instrumentator:
        # Expose metrics endpoint
        @app.get("/metrics", tags=["Monitoring"])
        async def metrics():
            """Expose Prometheus metrics."""
            from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
            return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
    MONITORING_ENABLED = True
except ImportError:
    MONITORING_ENABLED = False
    def track_task_operation(*args, **kwargs):
        pass
    def update_task_gauges(*args, **kwargs):
        pass

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monitoring middleware for request tracking
@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add processing time header to all responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check() -> HealthResponse:
    """
    Health check endpoint to verify application and database status.
    
    Returns:
        HealthResponse: Application health status
    """
    db_status = "healthy" if check_db_connection() else "unhealthy"
    app_status = "healthy" if db_status == "healthy" else "degraded"
    
    return HealthResponse(
        status=app_status,
        database=db_status,
        version=settings.app_version
    )


@app.get("/healthz", tags=["Health"])
def healthz() -> dict:
    """
    Kubernetes-style health check endpoint.
    
    Returns:
        dict: Simple status response
    """
    return {"status": "ok"}


# Task CRUD endpoints
@app.post(
    "/tasks/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task"
)
def add_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskSchema:
    """
    Create a new task.
    
    Args:
        task: Task creation data
        db: Database session dependency
        
    Returns:
        Created task
    """
    try:
        result = create_task(db=db, task=task)
        track_task_operation("create", "success")
        return result
    except Exception as e:
        track_task_operation("create", "error")
        raise


@app.get(
    "/tasks/{task_id}",
    response_model=TaskSchema,
    tags=["Tasks"],
    summary="Get a specific task"
)
def read_task(task_id: int, db: Session = Depends(get_db)) -> TaskSchema:
    """
    Retrieve a specific task by ID.
    
    Args:
        task_id: Task identifier
        db: Database session dependency
        
    Returns:
        Task details
        
    Raises:
        HTTPException: If task not found
    """
    db_task = get_task(db=db, task_id=task_id)
    if db_task is None:
        track_task_operation("read", "not_found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    track_task_operation("read", "success")
    return db_task


@app.get(
    "/tasks/",
    response_model=List[TaskSchema],
    tags=["Tasks"],
    summary="Get all tasks"
)
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[TaskSchema]:
    """
    Retrieve all tasks with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session dependency
        
    Returns:
        List of tasks
    """
    tasks = get_tasks(db=db, skip=skip, limit=limit)
    return tasks


@app.put(
    "/tasks/{task_id}",
    response_model=TaskSchema,
    tags=["Tasks"],
    summary="Update a task"
)
def update_existing_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
) -> TaskSchema:
    """
    Update an existing task.
    
    Args:
        task_id: Task identifier
        task: Task update data
        db: Database session dependency
        
    Returns:
        Updated task
        
    Raises:
        HTTPException: If task not found
    """
    db_task = update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@app.delete(
    "/tasks/{task_id}",
    response_model=TaskSchema,
    tags=["Tasks"],
    summary="Delete a task"
)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)) -> TaskSchema:
    """
    Delete a task.
    
    Args:
        task_id: Task identifier
        db: Database session dependency
        
    Returns:
        Deleted task
        
    Raises:
        HTTPException: If task not found
    """
    db_task = delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


# Statistics endpoint
@app.get("/tasks/stats/summary", tags=["Statistics"])
def get_task_statistics(db: Session = Depends(get_db)) -> dict:
    """
    Get task statistics.
    
    Args:
        db: Database session dependency
        
    Returns:
        Task statistics including total, completed, and pending counts
    """
    total = TaskRepository.count(db)
    completed = db.query(Task).filter(Task.completed == True).count()
    pending = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending
    }


# Static files and root endpoint
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/", tags=["Root"])
def read_index():
    """Serve the main application page."""
    return FileResponse("app/static/index.html")