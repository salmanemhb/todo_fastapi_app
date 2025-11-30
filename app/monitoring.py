"""
Monitoring and metrics module using Prometheus.
Provides instrumentation for tracking application performance.
"""
from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from fastapi import FastAPI
from app.config import get_settings

settings = get_settings()

# Custom metrics
task_operations = Counter(
    'task_operations_total',
    'Total number of task operations',
    ['operation', 'status']
)

active_tasks = Gauge(
    'active_tasks_total',
    'Total number of active (incomplete) tasks'
)

completed_tasks = Gauge(
    'completed_tasks_total',
    'Total number of completed tasks'
)

request_duration = Histogram(
    'request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)


def setup_metrics(app: FastAPI) -> Instrumentator:
    """
    Configure Prometheus metrics for the FastAPI application.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        Configured Instrumentator instance
    """
    if not settings.enable_metrics:
        return None
    
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics", "/health", "/healthz"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="http_requests_inprogress",
        inprogress_labels=True,
    )
    
    # Add default metrics
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    instrumentator.add(
        metrics.response_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    instrumentator.add(
        metrics.latency(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    instrumentator.add(
        metrics.requests(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True,
        )
    )
    
    # Instrument the app
    instrumentator.instrument(app)
    
    return instrumentator


def track_task_operation(operation: str, status: str = "success"):
    """
    Track task operations for monitoring.
    
    Args:
        operation: Type of operation (create, read, update, delete)
        status: Operation status (success, error)
    """
    task_operations.labels(operation=operation, status=status).inc()


def update_task_gauges(active: int, completed: int):
    """
    Update task count gauges.
    
    Args:
        active: Number of active tasks
        completed: Number of completed tasks
    """
    active_tasks.set(active)
    completed_tasks.set(completed)
