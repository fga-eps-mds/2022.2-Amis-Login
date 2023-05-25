from src.domain.models.social_worker import SocialWorkerDB  # certo
from src.domain.repositories import social_worker_repository
from src.infrastructure.repositories.field_repository import FieldValidation
from sqlalchemy.orm import Session

class SocialWorkerRepository:
    database: Session

    def __init__(self, session: Session):
        # TODO : usar o get db.
        self.database = session

    def find_all(self) -> list[SocialWorkerDB]:
        '''Função para fazer uma query de todas as SocialWorker da DB'''
        return self.database.query(SocialWorkerDB).all()

    def save(self, SocialWorkerSent: SocialWorkerDB) -> SocialWorkerDB:
        '''Função para salvar um objeto assistente na DB, utilizada também como update'''
        # TODO : verificar se o URM possui isso built in
        if self.find_by_login(SocialWorkerSent.login):
            self.database.merge(SocialWorkerSent)
        else:
            self.database.add(SocialWorkerSent)

        self.database.commit()
        print("Foda: ", SocialWorkerSent)
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

    def validateSocialWorker(self, socialWorker: SocialWorkerDB) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''

        fieldInfoDict = {}
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            socialWorker.nome))
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(
            socialWorker.login))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            socialWorker.senha))
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(socialWorker.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
            socialWorker.dNascimento))
        fieldInfoDict["observacao"] = vars(FieldValidation.observacaoValidation(
            socialWorker.observacao))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            socialWorker.telefone))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            socialWorker.email))
        # fieldInfoDict["administrador"] = FieldValidation.administradorValidation(
        # socialWorker.administrador)

        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict

assert isinstance(SocialWorkerRepository({}), social_worker_repository.SocialWorkerRepositoryBaseModel)
