from pydantic import BaseModel
from enum import Enum
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index
from sqlalchemy import Column, Enum as EnumDB


class SupervisorBase(BaseModel):
    login: str 
    nome: str
    senha: str
    data_nascimento: str
    cpf: str
    telefone: str
    email: str
    senha: str


class SupervisorRequest(SupervisorBase):
    ...


class SupervisorResponse(SupervisorBase):
    login: str

    class Config:
        orm_mode = True


class Supervisor(Base):
    __tablename__ = "supervisor"
    __table_args__ = {"extend_existing": True}

    login: str = Column(String(70), primary_key=True, nullable=False)
    nome: str = Column(String(70), nullable=False)
    data_nascimento: str = Column(String(10), nullable=False)
    cpf: str = Column(String(11), nullable=False)
    telefone: str = Column(String(11), nullable=False)
    email: str = Column(String(256), nullable=True)
    senha: str = Column(String(128), nullable=False)

