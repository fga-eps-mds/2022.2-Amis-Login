from domain.repositories.supervisor_repository import SupervisorRepository
from domain.models.supervisor import Supervisor, SupervisorBase, SupervisorRequest
from domain.repositories.tokens_repository import TokensRepositoryBaseModel
from infrastructure.repositories.field_repository import FieldValidation

from security import verify_password
from fastapi import HTTPException


class SupervisorService():
    __supervisorService__: SupervisorRepository
    __tokensRepository__: TokensRepositoryBaseModel

    def __init__(
        self, supervisorRepository: SupervisorRepository,
        tokensRepository: TokensRepositoryBaseModel
    ):
        self.__supervisorRepository__ = supervisorRepository
        self.__tokensRepository__ = tokensRepository

    def login(self, username: str, password: str) -> tuple[str, str]:
        supervisor = self.__supervisorRepository__.find_by_login_supervisor(username)
        if not supervisor or not verify_password(password, supervisor.senha):
            raise HTTPException(
                status_code=401,
                detail="Email ou nome de usuário incorretos"
            )

        userToken = self.__tokensRepository__.createUserToken(supervisor.login)
        refreshToken = self.__tokensRepository__.createRefreshToken(
            supervisor.login)

        return (userToken, refreshToken)

    def verifyToken(self, token: str) -> SupervisorBase:
        userLogin = self.__tokensRepository__.verifyToken(token=token)
        supervisor = self.__supervisorRepository__.find_by_login_supervisor(userLogin)

        return supervisor

    def refreshSession(self, refresh_token: str) -> tuple[str, str] | None:
        print("Token recebido: ", refresh_token)
        isRefreshTokenValid = self.__tokensRepository__.verifyToken(
            token=refresh_token)

        if isRefreshTokenValid:
            return self.__tokensRepository__.refreshToken(refresh_token=refresh_token)
        return None

    def find_by_login(self, login: str) -> Supervisor | None:
        return self.__supervisorRepository__.find_by_login_supervisor(login)
    
    def find_all(self) -> list[Supervisor]:
        supervisor_db = self.__supervisorRepository__.find_all_supervisor()
        supervisors = list()

        for supervisor_db in supervisor_db:
            supervisor = Supervisor(
                login=supervisor_db.login,
                nome=supervisor_db.nome,
                data_nascimento= supervisor_db.data_nascimento,
                cpf= supervisor_db.cpf,
                telefone= supervisor_db.telefone,
                email=supervisor_db.email,
                senha=supervisor_db.senha,
            )
            supervisors.append(supervisor)
        return supervisors
    
    def exists_by_login(self, login: str) -> bool:
        '''Função para verificar se existe um objeto SocialWorker com o login dado'''
        return self.__supervisorRepository__.find_by_login_supervisor(login) is not None

    def delete_refresh_token(self, refresh_token: str):
        self.__tokensRepository__.delete_refresh_token(refresh_token)
        return None

    def save(self, supervisor: Supervisor) -> Supervisor:
        '''Função para salvar um objeto SocialWorker na DB, utilizada também como update'''
        return self.__supervisorRepository__.save_supervisor(supervisor)

    def delete_by_login(self, login: str) -> None:
        '''Função para excluir um objeto SocialWorker da DB dado o login'''
        self.__supervisorRepository__.delete_by_login_supervisor(login)

    
    def validate_supervisor(self, supervisor: Supervisor) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''

        fieldInfoDict = {}
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(supervisor.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
        supervisor.data_nascimento))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            supervisor.email))
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(
            supervisor.login))
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            supervisor.nome))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            supervisor.senha))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            supervisor.telefone))
        
        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict
        