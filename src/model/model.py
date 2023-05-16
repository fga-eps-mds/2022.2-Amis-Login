'''Importando parâmetros da orm'''
from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base

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
    __tablename__ = "aluno"

    id_aluno : int = Column(Integer, primary_key = True, index = True)
    bairro : str = Column(String(50), nullable = False)
    cep : str = Column(String(10), nullable = False)
    cidade : str = Column(String(50), nullable = False)
    cpf : str = Column(String(11), nullable = False)
    data_nascimento : str = Column(String(10), nullable = False)
    deficiencia : bool = Column(Boolean, nullable = False)
    descricao_endereco : str = Column(String(100), nullable = False)
    email : str = Column(String(256), nullable = False)
    nome : str = Column(String(70) , nullable = False)
    nome_social : str = Column(String(70) , nullable = False)
    rg : str = Column(String(7), nullable = False)
    senha : str = Column(String(128), nullable = False)
    

class Telefone(Base):
    __tablename__ = "telefone"

    id_telefone : int = Column(Integer, primary_key = True, index = True)
    ddd :  int = Column(Integer, nullable = False)
    numero : str = Column(String(9), nullable = False)
    tipo_numero : str = Column(String(8), nullable = False)

