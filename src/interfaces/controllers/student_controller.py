from fastapi import APIRouter, HTTPException, status, Response
from interfaces.controllers import studentService

from typing import List

from domain.models.student import Student
from database import engine, Base
from domain.models.student import StudentRequest, StudentResponse
from security import get_password_hash

Base.metadata.create_all(bind=engine)

router_student = APIRouter(
  prefix = '/student',
  tags = ['student'],
  responses = {404: {"description": "Not found"}},
)



### student ###
@router_student.post("/", response_model = StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(request: StudentRequest):
    fieldsValidation = studentService.validate_student(Student(**request.dict()))
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    studentModel = Student(**request.dict())
    studentModel.senha = get_password_hash(studentModel.senha) 

    if studentService.exists_by_login(studentModel.login):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login já cadastrado") 
       
    student = studentService.save(studentModel)
    return StudentResponse.from_orm(student)
    

@router_student.get("/", response_model=List[StudentResponse]) 
def find_all_student():
    student = studentService.find_all()
    return[StudentResponse.from_orm(student) for student in student]

@router_student.get("/{login}", response_model = StudentResponse)
def find_by_login_student(login : str):
    student = studentService.find_by_login(login)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "student não encontrado"
        )
    return StudentResponse.from_orm(student)

@router_student.put("/{login}", response_model= StudentResponse)
def update_student_by_login(request: StudentRequest):
    fieldsValidation = studentService.validate_student(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    login = request.login
    if not studentService.exists_by_login(login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="student não encontrado")
    
    student = studentService.save(Student(**request.dict()))
    return StudentResponse.from_orm(student)


@router_student.delete("/{login}", status_code= status.HTTP_204_NO_CONTENT)
def delete_student_by_login(login : str):
    if not studentService.exists_by_login(login):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="student não encontrado"
        )
    studentService.delete_by_login(login)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
