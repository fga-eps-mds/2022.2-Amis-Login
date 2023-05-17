from ...domain.models.social_worker import SocialWorker

class SocialWorkerRepositoryBaseModel:
    def find_by_login(login: str) -> SocialWorker | None:
        '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
        pass 