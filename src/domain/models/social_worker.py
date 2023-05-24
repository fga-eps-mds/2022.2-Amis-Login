from src.database import Base
#from ...database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean


class SocialWorkerDB(Base):
    '''Classe para estabelecer o modelo da tabela na DB'''
    __tablename__ = "social_worker"
    __table_args__ = {"extend_existing": True}

    nome: str = Column(String(100), nullable=False)
    login: str = Column(String(100),primary_key=True, nullable=False)
    senha: str = Column(String(100), nullable=False)
    cpf: str = Column(String(11), nullable=False)
    dNascimento: str = Column(String(10), nullable=False)
    observacao: str = Column(String(200), nullable=True)
    telefone: str = Column(String(11), nullable=False)
    email: str = Column(String(100), nullable=True)
    administrador: bool = Column(Boolean, nullable=False)



class SocialWorker(BaseModel):
    nome: str
    login: str
    senha: str
    cpf: str
    dNascimento: str
    observacao: str
    email: str
    telefone: str
    administrador: bool


class SocialWorkerRequest(SocialWorker):
    '''...'''
    pass


class SocialWorkerResponse(SocialWorker):
    '''...'''
    class Config:
        orm_mode = True