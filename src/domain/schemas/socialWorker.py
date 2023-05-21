from typing import Union
from pydantic import BaseModel

class SocialWorker(BaseModel):
    '''Classe para definir os modelos recebidos na API'''
    nome: str
    cpf: str 
    login: str
    senha: str
    dNascimento: str
    observacao: str
    administrador: bool
    telefone: str
    email: str 

class SocialWorkerRequest(SocialWorker):
    '''...'''
    pass

class SocialWorkerResponse(SocialWorker):
    '''...'''
    class Config:
        orm_mode = True