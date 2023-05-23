from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from ...database import Base

class TeacherBase(BaseModel):
    codigo : str
    cpf : str
    cursos : str
    data_nascimento : str
    email : str
    nome : str
    telefone : str

class TeacherRequest(TeacherBase):
    ...

class TeacherResponse(TeacherBase):
    codigo : str

    class Config:
        orm_mode = True

class Teacher(Base):
    __tablename__ = "teachers"

    codigo : str = Column(String(70), primary_key = True, nullable = False)
    cpf : str = Column(String(11), nullable = False)
    cursos : str = Column(String(70), nullable = True)
    data_nascimento : str = Column(String(10), nullable = False)
    email : str = Column(String(256), nullable = True)
    nome : str = Column(String(70) , nullable = False)
    telefone : str = Column(String(11), nullable = False)
