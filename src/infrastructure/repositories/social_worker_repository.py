from ...domain.repositories.social_worker_repository  import SocialWorkerRepositoryBaseModel
from ...domain.models.social_worker import SocialWorker

class SocialWorkerRepository(SocialWorkerRepositoryBaseModel):
    __SocialWorkers__: list[SocialWorker] = []

    def find_by_login(self,login: str) -> SocialWorker | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        # return database.query(SocialWorker).filter(SocialWorker.login == login).first()
        for socialWorker in self.__SocialWorkers__:
            if socialWorker.login == login:
                return socialWorker
        return None