from domain.models.social_worker import SocialWorkerDB, SocialWorker  # certo
from infrastructure.repositories.field_repository import FieldValidation
from database import SessionLocal
from sqlalchemy.orm import Session


class SocialWorkerRepository:
    database: Session

    def __init__(self):
        # TODO : usar o get db.
        self.database = SessionLocal()

    def find_all(self) -> list[SocialWorkerDB]:
        '''Função para fazer uma query de todas as SocialWorker da DB'''
        return self.database.query(SocialWorkerDB).all()

    def save(self, SocialWorkerSent: SocialWorkerDB) -> SocialWorkerDB:
        '''Função para salvar um objeto assistente na DB, utilizada também como update'''

        # TODO : verificar se o URM possui isso built in
        if self.find_by_login(SocialWorkerDB.login):
            self.database.merge(SocialWorkerSent)
        else:
            self.database.add(SocialWorkerSent)

        self.database.commit()
        return SocialWorkerSent

    def find_by_login(self, login: str) -> SocialWorkerDB | None:
        '''Função para fazer uma query por login de um objeto assistente na DB'''
        return self.database.query(SocialWorkerDB).filter(SocialWorkerDB.login == login).first()

    def delete_by_login(self, login: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o login'''
        SocialWorkerObj = self.database.query(SocialWorkerDB).filter(
            SocialWorkerDB.login == login).first()

        if SocialWorkerObj is not None:
            self.database.delete(SocialWorkerObj)
            self.database.commit()


assert isinstance(SocialWorkerRepository(), SocialWorkerRepository)
