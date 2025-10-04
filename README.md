# To-Do List Application with FastAPI and SQLite

This is a minimal To-Do list application built using FastAPI and SQLite. The application provides a RESTful API for managing tasks, allowing users to create, read, update, and delete tasks.

## Features

- Create a new task
- Retrieve a list of tasks
- Update an existing task
- Delete a task

## Project Structure

```
todo_fastapi_app
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── models.py        # SQLAlchemy models for tasks
│   ├── crud.py          # CRUD operations for tasks
│   ├── database.py      # Database connection and session management
│   └── schemas.py       # Pydantic schemas for request and response validation
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd todo_fastapi_app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

- **Create a Task**: `POST /tasks`
- **Get All Tasks**: `GET /tasks`
- **Get a Task by ID**: `GET /tasks/{task_id}`
- **Update a Task**: `PUT /tasks/{task_id}`
- **Delete a Task**: `DELETE /tasks/{task_id}`

## License

This project is licensed under the MIT License.