from sqlalchemy.orm import Session
from model.model import Assistentes

class AssistentesRepository:
    @staticmethod
    def find_by_login(database: Session, login: str) -> Assistentes:
        '''Função para fazer uma query por login de um objeto Assistentes na DB'''
        return database.query(Assistentes).filter(Assistentes.login == login).first()