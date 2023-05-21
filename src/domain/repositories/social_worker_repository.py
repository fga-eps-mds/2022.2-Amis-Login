from ...domain.models.social_worker import SocialWorker
from typing import Protocol, runtime_checkable

@runtime_checkable
class SocialWorkerRepositoryBaseModel(Protocol):
    
    def find_by_login(self, login: str) -> SocialWorker | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        ...
