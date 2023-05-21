from domain.models.social_worker import SocialWorker
from typing import Protocol, runtime_checkable
from sqlalchemy.orm import Session

@runtime_checkable
class SocialWorkerRepositoryBaseModel(Protocol):
    
    def find_by_login(self, login: str) -> SocialWorker | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        ...

    @staticmethod
    def find_all(database: Session) -> list[SocialWorker]:
        '''Função para fazer uma query de todas as assistentes da DB'''
        return database.query(SocialWorker).all()

    @staticmethod
    def save(database: Session, socialworkers: SocialWorker) -> SocialWorker:
        '''Função para salvar um objeto assistente na DB'''
        if SocialWorkerRepositoryBaseModel.exists_by_cpf(database, socialworkers.cpf):
            database.merge(socialworkers)
        else:
            database.add(socialworkers)
        database.commit()
        return socialworkers

    @staticmethod
    def find_by_cpf(database: Session, cpf: str) -> SocialWorker:
        '''Função para fazer uma query por CPF de um objeto assistente na DB'''
        return database.query(SocialWorker).filter(SocialWorker.cpf == cpf).first()

    @staticmethod
    def exists_by_cpf(database: Session, cpf: str) -> bool:
        '''Função que verifica se o CPF dado existe na DB'''
        return database.query(SocialWorker).filter(SocialWorker.cpf == cpf).first() is not None

    @staticmethod
    def delete_by_cpf(database: Session, cpf: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o CPF'''
        socialworkers = database.query(SocialWorker).filter(
            SocialWorker.cpf == cpf).first()
        if socialworkers is not None:
            database.delete(socialworkers)
            database.commit()
