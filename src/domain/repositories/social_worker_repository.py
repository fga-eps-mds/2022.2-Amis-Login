from ...domain.models.social_worker import Assistentes

class SocialWorkerRepositoryBaseModel:
    def find_by_login(login: str) -> Assistentes | None:
        '''Função para fazer uma query por login de um objeto Assistentes na DB'''
        pass 