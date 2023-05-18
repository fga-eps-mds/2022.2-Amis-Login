from pydantic import BaseModel
from enum import Enum

##### Aluno ####
class Status(Enum):
    PRODUCAO = 1
    CURSO = 2
    INATIVO = 3

class AlunoBase(BaseModel):
    bairro : str
    cep : str
    cidade : str
    cpf : str
    data_nascimento : str 
    deficiencia : bool 
    descricao_endereco : str 
    email : str 
    login : str
    nome : str 
    senha : str
    status : Status
    telefone : str
    

class AlunoRequest(AlunoBase):
    ...

class AlunoResponse(AlunoBase):
    login : str

    class Config:
        orm_mode = True
    
