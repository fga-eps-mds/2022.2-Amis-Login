from database import get_db
from sqlalchemy.orm import Session
from assistente.schema import AssistentesBase, AssistentesResponse, AssistentesRequest
from assistente.repository import AssistentesRepository
from model.model import Assistentes
from security import get_password_hash
from fastapi import APIRouter, Depends, status, HTTPException, Response

router = APIRouter(
    prefix="/assistente",
    tags=["assistente"]
)

# CREATE
@router.post("/",
             response_model=AssistentesResponse,
             status_code=status.HTTP_201_CREATED,)
def create(Assistente: AssistentesRequest, database: Session = Depends(get_db)):
    # TODO: Adicionar validação dos dados.
    assistentesModel = Assistentes(**Assistente.dict())
    assistentesModel.senha = get_password_hash(assistentesModel.senha)

    if AssistentesRepository.exists_by_cpf(database, assistentesModel.cpf):
        print("Já existe um CPF cadastrado")
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    assistentes = AssistentesRepository.save(
        database=database, assistentes=assistentesModel)
    print(assistentes)
    return assistentes


# READ ALL 
@router.get("/", response_model=list[AssistentesBase])
def find_all(database: Session = Depends(get_db)):
    '''Faz uma query de todos os objetos assistente na DB (sem paginação)'''
    assistentes = AssistentesRepository.find_all(database)
    return [AssistentesResponse.from_orm(assistente) for assistente in assistentes]

# READ BY CPF
@router.get("/{cpf}", response_model=AssistentesBase)
def find_by_cpf(cpf: str, database: Session = Depends(get_db)):
    '''Dado o CPF como parâmetro, encontra a assistente com esse CPF'''
    assistente = AssistentesRepository.find_by_cpf(database, cpf)
    if not assistente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    return AssistentesResponse.from_orm(assistente)

# UPDATE BY CPF
@router.put("/{cpf}", response_model=AssistentesBase)
def update(request: AssistentesRequest, database: Session = Depends(get_db)):
    '''Dado o CPF da assistente, atualiza os dados cadastrais na DB por meio do método PUT'''
    cpf = request.cpf
    if not AssistentesRepository.exists_by_cpf(database, cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    assistente = AssistentesRepository.save(
        database, Assistentes(**request.dict()))
    return AssistentesResponse.from_orm(assistente)

# DELETE BY CPF
@router.delete("/{cpf}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_cpf(cpf: str, database: Session = Depends(get_db)):
    '''Dado o ID da assistente, deleta o objeto da DB por meio do método DELETE'''
    if not AssistentesRepository.exists_by_cpf(database, cpf):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assistente não encontrada"
        )
    AssistentesRepository.delete_by_cpf(database, cpf)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

