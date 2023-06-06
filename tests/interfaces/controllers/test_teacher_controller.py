from fastapi import APIRouter, HTTPException, status, Response
from interfaces.controllers import teacherService

from typing import List

from domain.models.teacher import Teacher
from database import engine, Base
from domain.models.teacher import TeacherRequest, TeacherResponse
from security import get_password_hash

Base.metadata.create_all(bind=engine)

router_teacher = APIRouter(
  prefix = '/teacher',
  tags = ['teacher'],
  responses = {404: {"description": "Not found"}},
)

### teacher ###
@router_teacher.post("/", response_model = TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(request: TeacherRequest):
    fieldsValidation = teacherService.validate_teacher(Teacher(**request.dict()))
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    teacherModel = teacher(**request.dict())
    teacherModel.senha = get_password_hash(teacherModel.senha) 

    if teacherService.exists_by_login(teacherModel.login):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login já cadastrado") 
       
    teacher = teacherService.save(teacherModel)
    return TeacherResponse.from_orm(teacher)
    

@router_teacher.get("/", response_model=List[TeacherResponse]) 
def find_all_teacher():
    teacher = teacherService.find_all()
    return[TeacherResponse.from_orm(teacher) for teacher in teacher]

@router_teacher.get("/{login}", response_model = TeacherResponse)
def find_by_login_teacher(login : str):
    teacher = teacherService.find_by_login(login)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "teacher não encontrado"
        )
    return TeacherResponse.from_orm(teacher)

@router_teacher.put("/{login}", response_model= TeacherResponse)
def update_teacher_by_login(request: TeacherRequest):
    fieldsValidation = teacherService.validate_teacher(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    login = request.login
    if not teacherService.exists_by_login(login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="teacher não encontrado")
    
    teacher = teacherService.save(Teacher(**request.dict()))
    return TeacherResponse.from_orm(teacher)


@router_teacher.delete("/{login}", status_code= status.HTTP_204_NO_CONTENT)
def delete_teacher_by_login(login : str):
    if not teacherService.exists_by_login(login):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="teacher não encontrado"
        )
    teacherService.delete_by_login(login)
    return Response(status_code = status.HTTP_204_NO_CONTENT)