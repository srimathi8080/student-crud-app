from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Student
from schemas import StudentCreate, StudentRead, StudentUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Students Database CRUD API",
    description="A beginner-friendly student records API built with FastAPI and SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Students CRUD API is running",
        "docs": "/docs",
        "endpoints": "/students",
    }


@app.post("/students", response_model=StudentRead, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student_data: StudentCreate, db: Session = __import__("fastapi").Depends(get_db)):
    student = Student(**student_data.model_dump())
    db.add(student)
    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A student with this email already exists.")
    return student


@app.get("/students", response_model=list[StudentRead], tags=["Students"])
def list_students(
    name: Optional[str] = Query(default=None, description="Filter by part of a student's name"),
    course: Optional[str] = Query(default=None, description="Filter by course"),
    db: Session = __import__("fastapi").Depends(get_db),
):
    statement = select(Student)
    if name:
        statement = statement.where(Student.name.ilike(f"%{name}%"))
    if course:
        statement = statement.where(Student.course.ilike(f"%{course}%"))
    return list(db.scalars(statement.order_by(Student.id)).all())


@app.get("/students/{student_id}", response_model=StudentRead, tags=["Students"])
def get_student(student_id: int, db: Session = __import__("fastapi").Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@app.put("/students/{student_id}", response_model=StudentRead, tags=["Students"])
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = __import__("fastapi").Depends(get_db),
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    updates = student_data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="Provide at least one field to update.")

    for field, value in updates.items():
        setattr(student, field, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A student with this email already exists.")
    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int, db: Session = __import__("fastapi").Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
