from sqlalchemy.orm import Session
from ..models.student import Student
from typing import List, runtime_checkable, Protocol
from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response
from ...infrastructure.repositories.field_repository import FieldValidation


@runtime_checkable
class StudentRepository(Protocol):
    
    def save_student(db: Session, student: Student) -> Student:
        ...

    def find_all_student(db: Session) -> List[Student]:
        ...

    def find_by_login_student(db : Session, login : str) -> Student:
        ...

    def exists_by_cpf_student(db: Session, cpf: str) -> bool:
        ...

    def delete_by_login_student(db: Session, login: str) -> None:
        ...

    def update_by_login(db: Session, student_request: Student) -> Student:
        ...

    def validate_student(student: Student) -> dict:
        ...