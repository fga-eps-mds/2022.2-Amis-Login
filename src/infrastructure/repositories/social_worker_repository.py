import sys
from pathlib import Path
# Adiciona o diretório "src" ao caminho de importação
sys.path.append(str(Path(__file__).resolve().parents[3]))
#from src.domain.models.social_worker import SocialWorkerDB
#from src.domain.models.social_worker import SocialWorkerDB  # certo
from ...domain.models.social_worker import SocialWorkerDB
from os import getenv
from src.security import get_password_hash
#from src.domain.repositories.social_worker_repository import SocialWorkerRepository
from ...domain.repositories.social_worker_repository import SocialWorkerRepository
#from domain.repositories.social_worker_repository import SocialWorkerRepository


class SocialWorkerRepository():
    __SocialWorkers__: list[SocialWorkerDB] = []

    def __init__(self):
        if getenv("ENV") == 'DEV':
            self.__SocialWorkers__.append(SocialWorkerDB(
                nome="test",
                login="test",
                senha=get_password_hash("test"),
                cpf="test",
                observacao="test",
                email="test",
                dNascimento="test",
                telefone="test",
                administrador=True
            ))

    def find_by_login(self, login: str) -> SocialWorkerDB | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        # return database.query(SocialWorker).filter(SocialWorker.login == login).first()
        for socialWorker in self.__SocialWorkers__:
            if socialWorker.login == login:
                return socialWorker
        return None


assert isinstance(SocialWorkerRepository(), SocialWorkerRepository)
