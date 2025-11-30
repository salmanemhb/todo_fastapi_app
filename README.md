# TODO FastAPI Application

[![CI/CD Pipeline](https://github.com/salmanemhb/todo_fastapi_app/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/salmanemhb/todo_fastapi_app/actions)
[![Code Coverage](https://img.shields.io/badge/coverage-70%25-brightgreen)](./htmlcov/index.html)
[![Python Version](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688)](https://fastapi.tiangolo.com/)

A modern, production-ready TODO application built with FastAPI, featuring comprehensive testing, monitoring, and DevOps best practices.

## 🚀 Features

- **RESTful API** with FastAPI
- **CRUD Operations** for task management
- **Health Checks** with database connectivity verification
- **Prometheus Metrics** for monitoring and observability
- **Comprehensive Testing** with 70%+ code coverage
- **Docker Support** with multi-stage builds
- **CI/CD Pipeline** with GitHub Actions
- **Code Quality** tools (Black, Flake8, Pylint)
- **Interactive API Documentation** (Swagger UI and ReDoc)

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Monitoring](#monitoring)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🏗️ Architecture

The application follows SOLID principles and clean architecture:

```
todo_fastapi_app/
├── app/
│   ├── config.py          # Configuration management
│   ├── database.py        # Database setup and sessions
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Repository pattern for data access
│   ├── main.py            # FastAPI application and routes
│   ├── monitoring.py      # Prometheus metrics
│   └── static/            # Frontend files
├── tests/                 # Comprehensive test suite
├── .github/workflows/     # CI/CD pipeline
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Container orchestration
└── prometheus.yml         # Monitoring configuration
```

## ✅ Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Docker and Docker Compose (optional, for containerized deployment)
- Git

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/salmanemhb/todo_fastapi_app.git
cd todo_fastapi_app
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional)
```

## 🏃 Running the Application

### Local Development

```bash
# Run with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html --cov-report=term
```

### View Coverage Report

```bash
# Open htmlcov/index.html in your browser
```

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/test_crud.py

# Integration tests only
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

### Test Coverage Targets

- **Minimum Coverage**: 70%
- **Current Coverage**: Check badge above or run `pytest --cov=app`

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the image
docker build -t todo-fastapi-app .

# Run the container
docker run -d -p 8000:8000 --name todo-app todo-fastapi-app
```

### Using Docker Compose (Recommended)

```bash
# Start all services (app + Prometheus + Grafana)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- **Application**: http://localhost:8000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## 📊 Monitoring

### Health Endpoints

- **Health Check**: `GET /health` - Returns application and database status
- **Kubernetes Health**: `GET /healthz` - Simple OK response

### Prometheus Metrics

- **Metrics Endpoint**: `GET /metrics`
- **Custom Metrics**:
  - `task_operations_total` - Total task operations by type
  - `active_tasks_total` - Current active tasks
  - `completed_tasks_total` - Total completed tasks
  - `http_requests_total` - Total HTTP requests
  - `request_duration_seconds` - Request latency histogram

### Accessing Monitoring Tools

1. **Prometheus UI**: http://localhost:9090
   - Query metrics
   - View targets
   - Create alerts

2. **Grafana Dashboards**: http://localhost:3000
   - Default credentials: admin/admin
   - Import FastAPI dashboard
   - Create custom visualizations

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Main Endpoints

#### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks/` | Create a new task |
| GET | `/tasks/` | Get all tasks (with pagination) |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

#### Statistics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/stats/summary` | Get task statistics |

#### Health & Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check with details |
| GET | `/healthz` | Simple health check |
| GET | `/metrics` | Prometheus metrics |

### Example Requests

#### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

#### Get All Tasks

```bash
curl -X GET "http://localhost:8000/tasks/?skip=0&limit=10"
```

#### Update a Task

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## 🗂️ Project Structure

```
todo_fastapi_app/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration with pydantic-settings
│   ├── database.py            # Database connection and session management
│   ├── models.py              # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic schemas for validation
│   ├── crud.py                # Repository pattern for data access
│   ├── main.py                # FastAPI app, routes, and middleware
│   ├── monitoring.py          # Prometheus metrics integration
│   └── static/
│       └── index.html         # Frontend UI
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures and configuration
│   ├── test_api.py            # API integration tests
│   ├── test_crud.py           # CRUD operation tests
│   ├── test_models.py         # Model tests
│   └── test_schemas.py        # Schema validation tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline
├── .dockerignore
├── .env.example               # Environment variables template
├── .gitignore
├── docker-compose.yml         # Multi-container setup
├── Dockerfile                 # Multi-stage Docker build
├── prometheus.yml             # Prometheus configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── setup.cfg                  # Testing and coverage configuration
└── README.md                  # This file
```

## 🔧 Development

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/ --max-line-length=100

# Type checking
mypy app/
```

### Pre-commit Checks

Before committing, ensure:
1. All tests pass: `pytest`
2. Coverage is above 70%: `pytest --cov=app`
3. Code is formatted: `black --check app/ tests/`
4. No linting errors: `flake8 app/ tests/`

## 🚀 CI/CD Pipeline

The GitHub Actions pipeline automatically:

1. **Code Quality**: Runs Black, Flake8, and Pylint
2. **Testing**: Executes all tests with coverage reporting
3. **Security**: Scans for vulnerabilities with Trivy
4. **Build**: Creates Docker image
5. **Deploy**: Deploys to production (on main branch)

### Pipeline Badges

- Build status, coverage, and security badges are displayed at the top of this README

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Salman** - *Initial work and DevOps implementation*

## 🙏 Acknowledgments

- FastAPI documentation and community
- Prometheus and Grafana teams
- IE University - Software Design & Development Operations course

## 📞 Support

For support, email your-email@example.com or open an issue in the repository.

---

**Note**: This application was developed as part of Individual Assignment 2 for the Software Design & Development Operations course at IE University, demonstrating DevOps best practices including testing, CI/CD, containerization, and monitoring.