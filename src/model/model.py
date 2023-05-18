'''Importando parâmetros da orm'''
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Index
from sqlalchemy import Column, Enum as EnumDB
from src.alunos.schemas import Status
from ..database import Base
from sqlalchemy.orm import relationship

class Assistentes(Base):
    '''Classe para estabelecer o modelo da tabela na DB'''
    __tablename__ = "assistentes"

    id: int = Column(Integer, primary_key = True, index = True)
    nome: str = Column(String(100), nullable = False)
    login: str = Column(String(100), nullable = False)
    senha: str = Column(String(100), nullable = False)
    cpf: str = Column(String(11), nullable = False)
    observacao: str = Column(String(200), nullable = True)
    administrador: bool = Column(Boolean, nullable = False)

class Aluno(Base):
    __tablename__ = "alunos"

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
    status = Column(EnumDB(Status), nullable=False)
    telefone : str = Column(String(11), nullable = False)


