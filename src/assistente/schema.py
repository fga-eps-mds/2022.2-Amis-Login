from typing import Union
from pydantic import BaseModel

class AssistentesBase(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    cpf: Union[str, None] = None
    login: str
    senha: str
    dNascimento: str
    observacao: str
    administrador: bool
    telefone: str
    email: str | None

class AssistentesRequest(AssistentesBase):
    '''...'''
    pass

class AssistentesResponse(AssistentesBase):
    '''...'''
    class Config:
        orm_mode = True