from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response
from sqlalchemy.orm import Session

from ..model.model import Aluno, Telefone
from ..database import engine, Base, get_db
from .repository import AlunoRepository, TelefoneRepository
from .schemas import AlunoRequest, AlunoResponse, TelefoneRequest, TelefoneResponse

Base.metadata.create_all(bind=engine)

router_alunos = APIRouter(
  prefix = '/alunos',
  tags = ['alunos'],
  responses = {404: {"description": "Not found"}},
)

### Aluno ###
@router_alunos.post("/", response_model = AlunoResponse, status_code=status.HTTP_201_CREATED)
def create_aluno(request: AlunoRequest, db: Session = Depends(get_db)):
    aluno = AlunoRepository.save_aluno(db, Aluno(**request.dict()))
    return AlunoResponse.from_orm(aluno)

@router_alunos.get("/", response_model=list[AlunoResponse]) 
def find_all_aluno(db: Session = Depends(get_db)):
    alunos = AlunoRepository.find_all_aluno(db)
    return[AlunoResponse.from_orm(alunos) for alunos in alunos]


@router_alunos.get("/{id}", response_model = AlunoResponse)
def find_by_id_aluno(id : int, db : Session =  Depends(get_db)):
    aluno = AlunoRepository.find_by_id_aluno(db, id)
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "Aluno não encontrado"
        )
    return AlunoResponse.from_orm(aluno)

@router_alunos.get("/cpf/{cpf}", response_model = AlunoResponse)
def find_by_cpf_aluno(cpf : str, db : Session =  Depends(get_db)):
    aluno = AlunoRepository.find_by_cpf_aluno(db, cpf)
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  detail = "Aluno não encontrado"
        )
    return AlunoResponse.from_orm(aluno)

@router_alunos.delete("/cpf/{cpf}", status_code= status.HTTP_204_NO_CONTENT)
def delete_aluno_by_cpf(cpf : str, db : Session =  Depends(get_db)):
    if not AlunoRepository.find_by_cpf_aluno(db, cpf):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado"
        )
    AlunoRepository.delete_by_cpf_aluno(db, cpf)
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router_alunos.put("/cpf/{cpf}", response_model= AlunoResponse)
def update_aluno_by_cpf(request: AlunoRequest, cpf: str, db : Session = Depends(get_db)):
    if not AlunoRepository.exists_by_cpf_aluno(db, cpf):
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado"
        )
    AlunoRepository.update_by_cpf(db, Aluno(**request.dict()))
    return Response(status_code= status.HTTP_404_NOT_FOUND)


### Telefone ###

router_telefone = APIRouter(
    prefix = '/telefone',
    tags = ['telefone'],
    responses = {404: {"description": "Not found"}},
)
@router_telefone.post("/", response_model=TelefoneResponse, status_code=status.HTTP_201_CREATED)
def create_telefone(request: TelefoneRequest, db: Session = Depends(get_db)):
     telefone = TelefoneRepository.save_telefone(db, Telefone(**request.dict()))
     return TelefoneResponse.from_orm(telefone)

@router_telefone.get("/", response_model=list[TelefoneResponse])
def find_all_telefone(db: Session = Depends(get_db)):
     telefones = TelefoneRepository.find_all_telefone(db)
     return[TelefoneResponse.from_orm(telefones) for telefones in telefones]


@router_telefone.get("/{id}", response_model = TelefoneResponse)
def find_by_id_telefone(id : int, db : Session =  Depends(get_db)):
     telefone = TelefoneRepository.find_by_id(db, id)
     if not telefone:
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,  detail = "Telefone não encontrado"
         )
     return AlunoResponse.from_orm(telefone)



