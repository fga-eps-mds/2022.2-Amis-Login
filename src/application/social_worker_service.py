from domain.models.social_worker import SocialWorker, SocialWorkerDB, SocialWorkerRequest
from domain.repositories.tokens_repository import TokensRepositoryBaseModel
from security import verify_password
from domain.repositories.social_worker_repository import SocialWorkerRepositoryBaseModel
from fastapi import HTTPException, status
from infrastructure.repositories.field_repository import FieldValidation


class SocialWorkerService():
    __socialWorkersRepository__: SocialWorkerRepositoryBaseModel
    __tokensRepository__: TokensRepositoryBaseModel

    def __init__(
        self,
        socialWorkersRepository: SocialWorkerRepositoryBaseModel,
        tokensRepository: TokensRepositoryBaseModel
    ):
        self.__socialWorkersRepository__ = socialWorkersRepository
        self.__tokensRepository__ = tokensRepository

    def login(self, username: str, password: str) -> tuple[str, str]:
        socialWorker = self.__socialWorkersRepository__.find_by_login(username)

        if not socialWorker or not verify_password(password, socialWorker.senha):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email ou nome de usuário incorretos"
            )

        userToken = self.__tokensRepository__.createUserToken(
            socialWorker.login)
        refreshToken = self.__tokensRepository__.createRefreshToken(
            socialWorker.login)

        return (userToken, refreshToken)

    def verifyToken(self, token: str) -> SocialWorker:
        userLogin = self.__tokensRepository__.verifyToken(token=token)
        socialWorker = self.__socialWorkersRepository__.find_by_login(
            userLogin)

        return socialWorker

    def refreshSession(self, refresh_token: str) -> tuple[str, str] | None:
        print("Token recebido: ", refresh_token)
        isRefreshTokenValid = self.__tokensRepository__.verifyToken(
            token=refresh_token)

        if isRefreshTokenValid:
            return self.__tokensRepository__.refreshToken(refresh_token=refresh_token)

        return None

    def find_by_login(self, login: str) -> SocialWorker | None:
        """Dado o login da assistente, retorna o objeto da assistente, ou None se não existir
        """
        return self.__socialWorkersRepository__.find_by_login(login=login)

    def find_all(self) -> list[SocialWorkerDB]:
        """Faz uma query de todos os objetos assistente na DB, 
        e retorna somente com os atributos Social Worker"""
        # father_attributes = {key: value for key, value in vars(child_obj).items() if key in vars(Father).keys()}
        social_workers_db = self.__socialWorkersRepository__.find_all()
        social_workers = list()
        for social_worker_db in social_workers_db:
            social_worker = SocialWorker(
                nome=social_worker_db.nome,
                login=social_worker_db.login,
                senha=social_worker_db.senha,
                cpf=social_worker_db.cpf,
                dNascimento=social_worker_db.dNascimento,
                observacao=social_worker_db.observacao,
                email=social_worker_db.email,
                telefone=social_worker_db.telefone,
                administrador=social_worker_db.administrador
            )
            social_workers.append(social_worker)
        return social_workers

    def validate_social_worker(self, social_worker: SocialWorkerRequest) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''

        fieldInfoDict = {}
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            social_worker.nome))
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(
            social_worker.login))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            social_worker.senha))
        fieldInfoDict["cpf"] = vars(
            FieldValidation.cpfValidation(social_worker.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
            social_worker.dNascimento))
        fieldInfoDict["observacao"] = vars(FieldValidation.observacaoValidation(
            social_worker.observacao))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            social_worker.telefone))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            social_worker.email))

        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict

    def exists_by_login(self, login: str) -> bool:
        '''Função para verificar se existe um objeto SocialWorker com o login dado'''
        return self.__socialWorkersRepository__.find_by_login(login=login) is not None

    def delete_refresh_token(self, refresh_token: str):
        self.__tokensRepository__.delete_refresh_token(refresh_token)
        return None

    def save(self, socialWorkerSent: SocialWorkerDB) -> SocialWorkerDB:
        '''Função para salvar um objeto SocialWorker na DB, utilizada também como update'''
        return self.__socialWorkersRepository__.save(socialWorkerSent=socialWorkerSent)

    def delete_by_login(self, login: str) -> None:
        '''Função para excluir um objeto SocialWorker da DB dado o login'''
        self.__socialWorkersRepository__.delete_by_login(login=login)
