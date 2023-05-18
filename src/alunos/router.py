from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session

from typing import List
from ..model.model import Aluno
from ..database import engine, Base, get_db
from .repository import AlunoRepository
from .schemas import AlunoRequest, AlunoResponse
from ..security import get_password_hash

Base.metadata.create_all(bind=engine)

router_alunos = APIRouter(
  prefix = '/alunos',
  tags = ['alunos'],
  responses = {404: {"description": "Not found"}},
)

### Aluno ###
@router_alunos.post("/", response_model = AlunoResponse, status_code=status.HTTP_201_CREATED)
def create_aluno(request: AlunoRequest, db: Session = Depends(get_db)):
    alunoModelo = Aluno(**request.dict())
    alunoModelo.senha = get_password_hash(alunoModelo.senha) 
    aluno = AlunoRepository.save_aluno(db, alunoModelo)
    return AlunoResponse.from_orm(aluno)

@router_alunos.get("/", response_model=List[AlunoResponse]) 
def find_all_aluno(db: Session = Depends(get_db)):
    alunos = AlunoRepository.find_all_aluno(db)
    return[AlunoResponse.from_orm(alunos) for alunos in alunos]

@router_alunos.get("/{login}", response_model = AlunoResponse)
def find_by_login_aluno(login : str, db : Session =  Depends(get_db)):
    aluno = AlunoRepository.find_by_login_aluno(db, login)
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "Aluno não encontrado"
        )
    return AlunoResponse.from_orm(aluno)

@router_alunos.delete("/{login}", status_code= status.HTTP_204_NO_CONTENT)
def delete_aluno_by_login(login : str, db : Session =  Depends(get_db)):
    if not AlunoRepository.find_by_login_aluno(db, login):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado"
        )
    AlunoRepository.delete_by_login_aluno(db, login)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router_alunos.put("/", response_model= AlunoResponse)
def update_aluno_by_login(request: AlunoRequest, db : Session = Depends(get_db)):

    aluno = AlunoRepository.update_by_login(db, request)
    return AlunoResponse.from_orm(aluno)

