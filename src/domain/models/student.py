from pydantic import BaseModel
from enum import Enum
from src.database import Base

'''Importando parâmetros da orm'''
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index
from sqlalchemy import Column, Enum as EnumDB


##### Aluno ####
class Status(Enum):
    PRODUCAO = 1
    CURSO = 2
    INATIVO = 3

class StudentBase(BaseModel):
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
    

class StudentRequest(StudentBase):
    ...

class StudentResponse(StudentBase):
    login : str

    class Config:
        orm_mode = True
    

class Student(Base):
    __tablename__ = "students"
    __table_args__ = {"extend_existing": True}

    bairro : str = Column(String(100), nullable = False)
    cep : str = Column(String(8), nullable = False)
    cidade : str = Column(String(100), nullable = False)
    cpf : str = Column(String(11), nullable = False)
    data_nascimento : str = Column(String(10), nullable = False)
    deficiencia : bool = Column(Boolean, nullable = False)
    descricao_endereco : str = Column(String(200), nullable = False)
    email : str = Column(String(256), nullable = True)
    nome : str = Column(String(70) , nullable = False)
    login : str = Column(String(70) , primary_key = True, nullable = False)
    senha : str = Column(String(128), nullable = False)
    status : Enum = Column(EnumDB(Status), nullable=False)
    telefone : str = Column(String(11), nullable = False)


