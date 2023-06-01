from domain.models.teacher import TeacherRequest, TeacherResponse
from domain.models.teacher import TeacherDB, Teacher
from security import get_password_hash
from fastapi import APIRouter, HTTPException, Response, status
from interfaces.controllers import teacherService

## Login vai ser chave primária

router_teacher = APIRouter(
  prefix = '/teacher',
  tags = ['teacher'],
  responses = {404: {"description": "Not found"}},
)

# CREATE

@router_teacher.post("/", response_model = TeacherResponse, status_code=status.HTTP_201_CREATED)
def create(teacher_request: TeacherRequest):
    fieldsValidation = teacherService.validate_teacher(teacher_request)

    if not fieldsValidation['completeStatus']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    teacher_model = TeacherDB(**teacher_request.dict())
    teacher_model.senha = get_password_hash(teacher_model.senha)

    if teacherService.exists_by_login(teacher_model.login):
        print("Já existe um código cadastrado")
        raise HTTPException(status_code=400, detail="código já cadastrado") 
       
    teacherService.save(teacher_model)

    return teacher_request

# READ ALL

@router_teacher.get("/", response_model=list[Teacher]) 
def find_all():
    teacher_DB = teacherService.find_all()
    return teacher_DB

# READ BY login

@router_teacher.get("/{login}", response_model = TeacherResponse)
def find_by_login(login : str):
    teacher = teacherService.find_by_login(login)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "Teacher não encontrado"
        )
    return TeacherResponse.from_orm(teacher)


# UPDATE BY login

@router_teacher.put("/{login}", response_model=TeacherResponse)
def update_by_login(request: TeacherRequest):
    fieldsValidation = teacherService.validate_teacher(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)

    login = request.login
    if not teacherService.exists_by_login(login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher não encontrado"
        )
    
    teacher_model = TeacherDB(**request.dict())
    teacher_model.senha = get_password_hash(teacher_model.senha)
    teacher = teacherService.save(teacher_model)

    return TeacherResponse.from_orm(teacher)

# DELETE BY login

@router_teacher.delete("/{login}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher_by_login(login: str):
    if not teacherService.exists_by_login(login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher não encontrado"
        )
    teacherService.delete_by_login(login)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


