from sqlalchemy.orm import Session
from model.model import Assistentes


class AssistentesRepository:
    @staticmethod
    def find_all(database: Session) -> list[Assistentes]:
        '''Função para fazer uma query de todas as assistentes da DB'''
        return database.query(Assistentes).all()

    @staticmethod
    def save(database: Session, assistentes: Assistentes) -> Assistentes:
        '''Função para salvar um objeto assistente na DB'''
        if AssistentesRepository.exists_by_cpf(database, assistentes.cpf):
            database.merge(assistentes)
        else:
            database.add(assistentes)
        database.commit()
        return assistentes

    @staticmethod
    def find_by_cpf(database: Session, cpf: str) -> Assistentes:
        '''Função para fazer uma query por CPF de um objeto assistente na DB'''
        return database.query(Assistentes).filter(Assistentes.cpf == cpf).first()

    @staticmethod
    def exists_by_cpf(database: Session, cpf: str) -> bool:
        '''Função que verifica se o CPF dado existe na DB'''
        return database.query(Assistentes).filter(Assistentes.cpf == cpf).first() is not None

    @staticmethod
    def delete_by_cpf(database: Session, cpf: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o CPF'''
        assistentes = database.query(Assistentes).filter(
            Assistentes.cpf == cpf).first()
        if assistentes is not None:
            database.delete(assistentes)
            database.commit()
