from sqlalchemy.orm import Session
from ..models.student import Student
from typing import List, runtime_checkable, Protocol


@runtime_checkable
class StudentRepository(Protocol):
    
    def save_student(self, student: Student) -> Student:
        ...

    def find_all_student(self) -> List[Student]:
        ...

    def find_by_login_student(self, login : str) -> Student:
        ...

    def exists_by_cpf_student(self, cpf: str) -> bool:
        ...

    def delete_by_login_student(self, login: str) -> None:
        ...

    def update_by_login(self, student_request: Student) -> Student:
        ...

    def validate_student(self, student: Student) -> dict:
        ...
