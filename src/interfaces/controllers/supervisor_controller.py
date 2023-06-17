from fastapi import APIRouter, HTTPException, status, Response
from interfaces.controllers import supervisorService

from typing import List

from domain.models.supervisor import Supervisor
from database import engine, Base
from domain.models.supervisor import SupervisorRequest, SupervisorResponse
from security import get_password_hash

Base.metadata.create_all(bind=engine)

router_supervisor = APIRouter(
  prefix = '/supervisor',
  tags = ['supervisor'],
  responses = {404: {"description": "Not found"}},
)

@router_supervisor.post("/", response_model = SupervisorResponse, status_code=status.HTTP_201_CREATED)
def create_supervisor(request: SupervisorRequest):
    fieldsValidation = supervisorService.validate_supervisor(Supervisor(**request.dict()))
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    supervisorModel = Supervisor(**request.dict())
    supervisorModel.senha = get_password_hash(supervisorModel.senha) 

    if supervisorService.exists_by_login(supervisorModel.login):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="login já cadastrado") 
       
    supervisor = supervisorService.save(supervisorModel)
    return SupervisorResponse.from_orm(supervisor)
    

@router_supervisor.get("/", response_model=List[SupervisorResponse]) 
def find_all_supervisor():
    supervisor = supervisorService.find_all()
    return[SupervisorResponse.from_orm(supervisor) for supervisor in supervisor]

@router_supervisor.get("/{login}", response_model = SupervisorResponse)
def find_by_login_supervisor(login : str):
    supervisor = supervisorService.find_by_login(login)
    if not supervisor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "supervisor não encontrado"
        )
    return SupervisorResponse.from_orm(supervisor)

@router_supervisor.put("/{login}", response_model= SupervisorResponse)
def update_supervisor_by_login(request: SupervisorRequest):
    fieldsValidation = supervisorService.validate_supervisor(request)
    if not fieldsValidation['completeStatus']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fieldsValidation)
    
    login = request.login
    if not supervisorService.exists_by_login(login):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="supervisor não encontrado")
    
    supervisor = supervisorService.save(Supervisor(**request.dict()))
    return SupervisorResponse.from_orm(supervisor)


@router_supervisor.delete("/{login}", status_code= status.HTTP_204_NO_CONTENT)
def delete_supervisor_by_login(login : str):
    if not supervisorService.exists_by_login(login):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="supervisor não encontrado"
        )
    supervisorService.delete_by_login(login)
    return Response(status_code = status.HTTP_204_NO_CONTENT)
