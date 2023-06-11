from pydantic import BaseModel
from sqlalchemy import Column, String
from database import Base

class TeacherDB(Base):
    '''Classe para estabelecer o modelo da tabela na DB'''
    __tablename__ = "teacher"
    __table_args__ = {"extend_existing": True}

    cpf : str = Column(String(11), nullable = False)
    habilidades : str = Column(String(70), nullable = True)
    data_nascimento : str = Column(String(10), nullable = False)
    email : str = Column(String(256), nullable = True)
    login : str = Column(String(70), primary_key = True, nullable = False)
    nome : str = Column(String(70) , nullable = False)
    senha : str = Column(String(128), nullable=False)
    telefone : str = Column(String(11), nullable = False)


class Teacher(BaseModel):
    
    cpf : str
    habilidades : str
    data_nascimento : str
    email : str
    login : str
    nome : str
    senha : str
    telefone : str

class TeacherRequest(Teacher):
    "..."
    pass

class TeacherResponse(Teacher):
    "..."

    class Config:
        orm_mode = True

