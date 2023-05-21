from domain.models.social_worker import SocialWorkerDB
from typing import Protocol, runtime_checkable
from sqlalchemy.orm import Session


@runtime_checkable
class SocialWorkerRepositoryBaseModel(Protocol):

    def find_by_login(self, login: str) -> SocialWorkerDB | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        ...


class SocialWorkerRepository:
    @staticmethod
    def find_all(database: Session) -> list[SocialWorkerDB]:
        '''Função para fazer uma query de todas as SocialWorker da DB'''
        return database.query(SocialWorkerDB).all()

    @staticmethod
    def save(database: Session, SocialWorkerSent: SocialWorkerDB) -> SocialWorkerDB:
        '''Função para salvar um objeto assistente na DB'''
        if SocialWorkerRepository.exists_by_cpf(database, SocialWorkerDB.cpf):

            database.merge(SocialWorkerSent)
        else:
            database.add(SocialWorkerSent)

        database.commit()
        return SocialWorkerSent

    @staticmethod
    def find_by_cpf(database: Session, cpf: str) -> SocialWorkerDB:
        '''Função para fazer uma query por CPF de um objeto assistente na DB'''
        return database.query(SocialWorkerDB).filter(SocialWorkerDB.cpf == cpf).first()

    @staticmethod
    def exists_by_cpf(database: Session, cpf: str) -> bool:
        '''Função que verifica se o CPF dado existe na DB'''
        return database.query(SocialWorkerDB).filter(SocialWorkerDB.cpf == cpf).first() is not None

    @staticmethod
    def delete_by_cpf(database: Session, cpf: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o CPF'''
        SocialWorkerObj = database.query(SocialWorkerDB).filter(
            SocialWorkerDB.cpf == cpf).first()

        if SocialWorkerObj is not None:
            database.delete(SocialWorkerObj)
            database.commit()
