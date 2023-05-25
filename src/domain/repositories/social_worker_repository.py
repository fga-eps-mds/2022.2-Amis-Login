from src.domain.models.social_worker import SocialWorkerDB, SocialWorker
from sqlalchemy.orm import Session
from typing import Protocol, runtime_checkable
from src.infrastructure.repositories.field_repository import FieldValidation


@runtime_checkable
class SocialWorkerRepositoryBaseModel(Protocol):
    # TODO : Remover o database, deixar mais genérico.
    def find_by_login(self, login: str) -> SocialWorkerDB | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        ...

    def find_all(self, database: Session) -> list[SocialWorkerDB]:
        '''Função para fazer uma query de todas as SocialWorker da DB'''
        ...

    def save(self, database: Session, SocialWorkerSent: SocialWorkerDB) -> SocialWorkerDB:
        '''Função para salvar um objeto assistente na DB'''
        ...

    def delete_by_login(self, database: Session, login: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o login'''
        ...

    def validateSocialWorker(self, socialWorker: SocialWorker) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''
        ...
