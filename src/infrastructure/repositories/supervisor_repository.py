from sqlalchemy.orm import Session
from domain.models.supervisor import Supervisor
from typing import List
from fastapi import HTTPException, status
from infrastructure.repositories.field_repository import FieldValidation
from domain.repositories import supervisor_repository
from typing import Callable

class SupervisorRepository:
    __db: Callable[[], Session]
    def __init__(self, session: Callable[[], Session]):
        self.__db = session

    def save_supervisor(self, supervisor: Supervisor) -> Supervisor:
        session = self.__db()
        if supervisor.login:
            session.merge(supervisor)
        else:
            session.add(supervisor)
        session.commit()
        return supervisor

    def find_all_supervisor(self) -> List[Supervisor]:
        return self.__db().query(Supervisor).all()
    
    def find_by_login_supervisor(self, login : str) -> Supervisor:
        return self.__db().query(Supervisor).filter(Supervisor.login == login).first()
    
    def exists_by_cpf_supervisor(self, cpf: str) -> bool:
        return self.__db().query(Supervisor).filter(Supervisor.cpf == cpf).first() is not None 

    def delete_by_login_supervisor(self, login: str) -> None:
        session = self.__db()
        supervisor = session.query(Supervisor).filter(Supervisor.login == login).first()
        if supervisor is not None:
            session.delete(supervisor)
            session.commit()
        return None

    def update_by_login(self, supervisor_request: Supervisor) -> Supervisor:

        supervisor = self.find_by_login_supervisor(self, login=supervisor_request.login) 
        if not supervisor:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="supervisor não encontrado"
        )

        supervisor.nome = supervisor_request.nome
        supervisor.data_nascimento = supervisor_request.data_nascimento
        supervisor.cpf = supervisor_request.cpf
        supervisor.telefone = supervisor_request.telefone
        supervisor.email = supervisor_request.email
        supervisor.senha = supervisor_request.senha
        
        self.save_supervisor(self, supervisor=supervisor)
        return supervisor

    def validate_supervisor(self, supervisor: Supervisor) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''

        fieldInfoDict = {}
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(
            supervisor.login))
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            supervisor.nome))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
        supervisor.data_nascimento))
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(supervisor.cpf))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            supervisor.telefone))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            supervisor.email))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            supervisor.senha))
        
        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict

assert isinstance(SupervisorRepository(session={}), supervisor_repository.SupervisorRepository)