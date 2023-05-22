from domain.models.social_worker import SocialWorkerDB, SocialWorker
from sqlalchemy.orm import Session

from infrastructure.repositories.field_repository import FieldValidation


# @runtime_checkable
# class SocialWorkerRepositoryBaseModel(Protocol):

# def find_by_login(self, login: str) -> SocialWorkerDB | None:
#    '''Função para fazer uma query por login de um objeto SocialWorker na DB'''
#    ...


class SocialWorkerRepository:
    @staticmethod
    def find_all(database: Session) -> list[SocialWorkerDB]:
        '''Função para fazer uma query de todas as SocialWorker da DB'''
        return database.query(SocialWorkerDB).all()

    @staticmethod
    def save(database: Session, SocialWorkerSent: SocialWorkerDB) -> SocialWorkerDB:
        '''Função para salvar um objeto assistente na DB'''
        if SocialWorkerRepository.exists_by_login(database, SocialWorkerDB.login):

            database.merge(SocialWorkerSent)
        else:
            database.add(SocialWorkerSent)

        database.commit()
        return SocialWorkerSent

    @staticmethod
    def find_by_login(database: Session, login: str) -> SocialWorkerDB:
        '''Função para fazer uma query por login de um objeto assistente na DB'''
        return database.query(SocialWorkerDB).filter(SocialWorkerDB.login == login).first()

    @staticmethod
    def exists_by_login(database: Session, login: str) -> bool:
        '''Função que verifica se o login dado existe na DB'''
        return database.query(SocialWorkerDB).filter(SocialWorkerDB.login == login).first() is \
            not None

    @staticmethod
    def delete_by_login(database: Session, login: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o login'''
        SocialWorkerObj = database.query(SocialWorkerDB).filter(
            SocialWorkerDB.login == login).first()

        if SocialWorkerObj is not None:
            database.delete(SocialWorkerObj)
            database.commit()

    @staticmethod
    def validateSocialWorker(socialWorker: SocialWorker) -> dict:
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
