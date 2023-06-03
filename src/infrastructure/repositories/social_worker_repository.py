from domain.models.social_worker import SocialWorkerDB  # certo
from domain.repositories import social_worker_repository
from infrastructure.repositories.field_repository import FieldValidation
from sqlalchemy.orm import Session
from typing import Callable


class SocialWorkerRepository:
    database: Callable[[], Session]

    def __init__(self, session: Callable[[], Session]):
        self.database = session

    def find_all(self) -> list[SocialWorkerDB]:
        '''Função para fazer uma query de todas as SocialWorker da DB'''
        session = self.database()
        res = session.query(SocialWorkerDB).all()
        session.close()
        return res

    def save(self, socialWorkerSent: SocialWorkerDB) -> SocialWorkerDB:
        '''Função para salvar um objeto assistente na DB, utilizada também como update'''
        session = self.database()
        # TODO : verificar se o URM possui isso built in
        if self.find_by_login(socialWorkerSent.login):
            session.merge(socialWorkerSent)
        else:
            session.add(socialWorkerSent)

        session.commit()
        session.expunge_all()
        session.close()
        return socialWorkerSent

    def find_by_login(self, login: str) -> SocialWorkerDB | None:
        '''Função para fazer uma query por login de um objeto assistente na DB'''
        session = self.database()
        return session.query(SocialWorkerDB).filter(SocialWorkerDB.login == login).first()

    def delete_by_login(self, login: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o login'''

        session = self.database()
        SocialWorkerObj = session.query(SocialWorkerDB).filter(
            SocialWorkerDB.login == login).first()

        if SocialWorkerObj is not None:
            session.delete(SocialWorkerObj)
            session.commit()

        session.close()

    def validateSocialWorker(self, socialWorker: SocialWorkerDB) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''

        fieldInfoDict = {}
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            socialWorker.nome))
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(
            socialWorker.login))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            socialWorker.senha))
        fieldInfoDict["cpf"] = vars(
            FieldValidation.cpfValidation(socialWorker.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
            socialWorker.dNascimento))
        fieldInfoDict["observacao"] = vars(FieldValidation.observacaoValidation(
            socialWorker.observacao))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            socialWorker.telefone))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            socialWorker.email))

        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict


assert isinstance(SocialWorkerRepository(
    {}), social_worker_repository.SocialWorkerRepositoryBaseModel)
