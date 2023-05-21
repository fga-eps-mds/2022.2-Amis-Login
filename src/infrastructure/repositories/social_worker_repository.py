from ...domain.models.social_worker import SocialWorker
from os import getenv
from src.security import get_password_hash
from ...domain.repositories.social_worker_repository import SocialWorkerRepositoryBaseModel

class SocialWorkerRepository():
    __SocialWorkers__: list[SocialWorker] = []

    def __init__(self):
        if getenv("ENV") == 'DEV':
            self.__SocialWorkers__.append(SocialWorker(
                id=1,
                nome="test",
                login="test",
                senha=get_password_hash("test"),
                cpf="test",
                observacao="test",
                administrador= True
            ))

    def find_by_login(self, login: str) -> SocialWorker | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        # return database.query(SocialWorker).filter(SocialWorker.login == login).first()
        for socialWorker in self.__SocialWorkers__:
            if socialWorker.login == login:
                return socialWorker
        return None

assert isinstance(SocialWorkerRepository(), SocialWorkerRepositoryBaseModel)
