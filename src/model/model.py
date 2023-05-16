'''Importando parâmetros da orm'''
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Assistentes(Base):
    '''Classe para estabelecer o modelo da tabela na DB'''
    __tablename__ = "assistentes"

    nome: str = Column(String(100), nullable=False)
    login: str = Column(String(100), nullable=False)
    senha: str = Column(String(100), nullable=False)
    cpf: str = Column(String(11), primary_key=True, nullable=False)
    dNascimento = Column(String(10), nullable=False)
    observacao = Column(String(200), nullable=True)
    telefone  =  Column(String(11), nullable=False)
    email = Column(String(100), nullable=True)
    administrador: bool = Column(Boolean, nullable=False)