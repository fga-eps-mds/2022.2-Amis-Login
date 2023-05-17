from ...domain.repositories.social_worker_repository  import SocialWorkerRepositoryBaseModel
from ...domain.models.social_worker import Assistentes

class SocialWorkerRepository(SocialWorkerRepositoryBaseModel):
    __assistentes__: list[Assistentes] = []
    @staticmethod
    def find_by_login(self,login: str) -> Assistentes | None:
        '''Função para fazer uma query por login de um objeto Assistentes na DB'''
        # return database.query(Assistentes).filter(Assistentes.login == login).first()
        for assistente in self.__assistentes__:
            if assistente.login == login:
                return assistente
        return None