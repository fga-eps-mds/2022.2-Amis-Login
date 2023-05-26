from fastapi import APIRouter, HTTPException, status, Response
from interfaces.controllers import studentRepository

from typing import List

from src.domain.models.student import Student
from src.database import engine, Base
from src.domain.models.student import StudentRequest, StudentResponse
from src.security import get_password_hash

Base.metadata.create_all(bind=engine)

router_student = APIRouter(
  prefix = '/student',
  tags = ['student'],
  responses = {404: {"description": "Not found"}},
)



### student ###
@router_student.post("/", response_model = StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(request: StudentRequest):
    fieldsValidation = studentRepository.validate_student(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    studentModel = Student(**request.dict())
    studentModel.senha = get_password_hash(studentModel.senha) 

    if studentRepository.exists_by_cpf_student(studentModel.cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login já cadastrado") 
       
    student = studentRepository.save_student(studentModel)
    return StudentResponse.from_orm(student)
    

@router_student.get("/", response_model=List[StudentResponse]) 
def find_all_student():
    student = studentRepository.find_all_student()
    return[StudentResponse.from_orm(student) for student in student]

@router_student.get("/{login}", response_model = StudentResponse)
def find_by_login_student(login : str):
    student = studentRepository.find_by_login_student(login)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "student não encontrado"
        )
    return StudentResponse.from_orm(student)

@router_student.delete("/{login}", status_code= status.HTTP_204_NO_CONTENT)
def delete_student_by_login(login : str):
    if not studentRepository.find_by_login_student(login):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="student não encontrado"
        )
    studentRepository.delete_by_login_student( login)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router_student.put("/", response_model= StudentResponse)
def update_student_by_login(request: StudentRequest):
    fieldsValidation = studentRepository.validate_student(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    cpf = request.cpf
    if not studentRepository.exists_by_cpf_student(cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="student não encontrado")
    
    student = studentRepository.update_by_login(request)
    return StudentResponse.from_orm(student)

