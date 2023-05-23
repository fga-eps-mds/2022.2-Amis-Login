from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session

from typing import List

from src.domain.repositories.student_repository import StudentRepository
from ...domain.models.student import Student
from ...database import engine, Base, get_db
from ...domain.models.student import StudentRequest, StudentResponse
from ...security import get_password_hash

Base.metadata.create_all(bind=engine)

router_student = APIRouter(
  prefix = '/student',
  tags = ['student'],
  responses = {404: {"description": "Not found"}},
)

### student ###
@router_student.post("/", response_model = StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(request: StudentRequest, db: Session = Depends(get_db)):
    fieldsValidation = StudentRepository.validate_student(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    studentModel = Student(**request.dict())
    studentModel.senha = get_password_hash(studentModel.senha) 

    if StudentRepository.exists_by_cpf_student(db, studentModel.cpf):
        print("Já existe um login cadastrado")
        raise HTTPException(status_code=400, detail="login já cadastrado") 
       
    student = StudentRepository.save_student(db, studentModel)
    return StudentResponse.from_orm(student)
    

@router_student.get("/", response_model=List[StudentResponse]) 
def find_all_student(db: Session = Depends(get_db)):
    student = StudentRepository.find_all_student(db)
    return[StudentResponse.from_orm(student) for student in student]

@router_student.get("/{login}", response_model = StudentResponse)
def find_by_login_student(login : str, db : Session =  Depends(get_db)):
    student = StudentRepository.find_by_login_student(db, login)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "student não encontrado"
        )
    return StudentResponse.from_orm(student)

@router_student.delete("/{login}", status_code= status.HTTP_204_NO_CONTENT)
def delete_student_by_login(login : str, db : Session =  Depends(get_db)):
    if not StudentRepository.find_by_login_student(db, login):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="student não encontrado"
        )
    StudentRepository.delete_by_login_student(db, login)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router_student.put("/", response_model= StudentResponse)
def update_student_by_login(request: StudentRequest, db : Session = Depends(get_db)):
    fieldsValidation = StudentRepository.validate_student(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    cpf = request.cpf
    if not StudentRepository.exists_by_cpf_student(db, cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="student não encontrado")
    
    student = StudentRepository.update_by_login(db, request)
    return StudentResponse.from_orm(student)

