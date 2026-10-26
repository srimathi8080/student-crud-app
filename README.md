# Students Database CRUD Application

A Python backend project for the EWB Edu Tech internship assignment. It uses **FastAPI** for the REST API and **SQLite** for persistent storage.

## Features

- Create student records
- List all students
- Search by part of a name or course
- Retrieve one student by ID
- Update student details
- Delete student records
- Input validation for dates, email addresses, and field lengths
- Clear `404` errors when a student does not exist
- Duplicate email protection
- Interactive API documentation at `/docs`

## Student fields

- `id`: automatically generated unique ID
- `name`: required
- `date_of_birth`: required, format `YYYY-MM-DD`
- `email`: required and unique
- `phone`: optional
- `course`: optional
- `address`: optional
- `enrollment_date`: optional, format `YYYY-MM-DD`

## Requirements

- Python 3.10 or newer
- pip

## Install and run

Open a terminal in this project folder.

### 1. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 2. Install packages

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn main:app --reload
```

Open:

- API home: http://127.0.0.1:8000/
- Interactive Swagger testing: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

The `students.db` SQLite database is created automatically when the application starts. It is excluded from Git using `.gitignore`.

## Test the endpoints in Swagger UI

Open `http://127.0.0.1:8000/docs`, expand an endpoint, click **Try it out**, provide the example input, and click **Execute**.

### Create a student — `POST /students`

```json
{
  "name": "Arun Kumar",
  "date_of_birth": "2005-06-15",
  "email": "arun@example.com",
  "phone": "9000000001",
  "course": "BSc Computer Science",
  "address": "Coimbatore",
  "enrollment_date": "2024-06-10"
}
```

### List students — `GET /students`

No request body is required.

Filter examples:

- `/students?name=Arun`
- `/students?course=Computer`

### Get one student — `GET /students/1`

Replace `1` with the ID returned when you create a student.

### Update a student — `PUT /students/1`

Only send fields you want to change. For example:

```json
{
  "course": "BSc Data Science"
}
```

### Delete a student — `DELETE /students/1`

Replace `1` with the ID of the record you want to delete. A successful delete returns HTTP `204`.

## Common response codes

- `201`: student created
- `200`: request succeeded
- `204`: student deleted successfully
- `400`: invalid update request
- `404`: student not found
- `409`: email already exists

FastAPI automatically returns `422` for invalid request data, such as an invalid email or date format.

## GitHub submission

1. Create a new GitHub repository named `students-crud-app`.
2. Do not add real student information or secrets.
3. From this project folder, run:

```bash
git init
git add .
git commit -m "Build student CRUD API with FastAPI and SQLite"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/students-crud-app.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL GitHub gives you.

## Optional AI extension

The Ollama integration is not included in this core version because it is optional in the assignment. First demonstrate that all CRUD endpoints work correctly. An AI extension can be added later using a local Ollama model, with database records retrieved safely by backend code rather than allowing the model to execute arbitrary SQL.

## Privacy

Use dummy/sample data only. The SQLite database is local and is intentionally ignored by Git.
