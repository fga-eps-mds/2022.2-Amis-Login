from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from src.domain.repositories.teacher_repository import TeacherRepository
from ...domain.models.teacher import Teacher
from ...database import engine, Base, get_db
from ...domain.models.teacher import TeacherRequest, TeacherResponse
from ...security import get_password_hash

Base.metadata.create_all(bind=engine)

router_teacher = APIRouter(
  prefix = '/teacher',
  tags = ['teacher'],
  responses = {404: {"description": "Not found"}},
)


@router_teacher.post("/", response_model = TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(request: TeacherRequest, db: Session = Depends(get_db)):
    fieldsValidation = TeacherRepository.validate_teacher(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    teacherModel = Teacher(**request.dict())
    if TeacherRepository.exists_by_codigo_teacher(db, teacherModel.cpf):
        print("Já existe um código cadastrado")
        raise HTTPException(status_code=400, detail="código já cadastrado") 
       
    teacher = TeacherRepository.save_teacher(db, teacherModel)
    return TeacherResponse.from_orm(teacher)

@router_teacher.get("/", response_model=List[TeacherResponse]) 
def find_all_teacher(db: Session = Depends(get_db)):
    teacher = TeacherRepository.find_all_teacher(db)
    return[TeacherResponse.from_orm(teacher) for teacher in teacher]

@router_teacher.get("/{codigo}", response_model = TeacherResponse)
def find_by_codigo_teacher(codigo : str, db : Session =  Depends(get_db)):
    teacher = TeacherRepository.find_by_codigo_teacher(db, codigo)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "teacher não encontrado"
        )
    return TeacherResponse.from_orm(teacher)

@router_teacher.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher_by_codigo(codigo: str, db: Session = Depends(get_db)):
    TeacherRepository.delete_by_codigo_teacher(db, codigo)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_teacher.put("/{codigo}", response_model=TeacherResponse)
def update_teacher_by_codigo(codigo: str, request: TeacherRequest, db: Session = Depends(get_db)):
    fieldsValidation = TeacherRepository.validate_teacher(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)

    teacher = TeacherRepository.update_by_codigo(db, request)
    return TeacherResponse.from_orm(teacher)