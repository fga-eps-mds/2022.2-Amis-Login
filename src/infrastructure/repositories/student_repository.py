from sqlalchemy.orm import Session
from domain.models.student import Student
from typing import List
from fastapi import HTTPException, status
from infrastructure.repositories.field_repository import FieldValidation
from domain.repositories import student_repository
from typing import Callable

class StudentRepository:
    __db: Callable[[], Session]
    def __init__(self, session: Callable[[], Session]):
        self.__db = session

    def save_student(self, student: Student) -> Student:
        session = self.__db()
        if student.login:
            session.merge(student)
        else:
            session.add(student)
        session.commit()
        return student

    def find_all_student(self) -> List[Student]:
        return self.__db().query(Student).all()
    
    def find_by_login_student(self, login : str) -> Student:
        return self.__db().query(Student).filter(Student.login == login).first()
    
    def exists_by_cpf_student(self, cpf: str) -> bool:
        return self.__db().query(Student).filter(Student.cpf == cpf).first() is not None 

    def delete_by_login_student(self, login: str) -> None:
        session = self.__db()
        student = session.query(Student).filter(Student.login == login).first()
        if student is not None:
            session.delete(student)
            session.commit()
        return None

    def update_by_login(self, student_request: Student) -> Student:

        student = self.find_by_login_student(self, login=student_request.login) 
        if not student:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="student não encontrado"
        )

        student.bairro = student_request.bairro
        student.cep = student_request.cep
        student.cidade = student_request.cidade
        student.cpf = student_request.cpf
        student.data_nascimento = student_request.data_nascimento
        student.deficiencia = student_request.deficiencia
        student.descricao_endereco = student_request.descricao_endereco
        student.email = student_request.email
        student.nome = student_request.nome
        student.senha = student_request.senha
        student.status = student_request.status
        student.telefone = student_request.telefone
        
        self.save_student(self, student=student)
        return student

    def validate_student(self, student: Student) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''

        fieldInfoDict = {}
        fieldInfoDict["bairro"] = vars(FieldValidation.bairroValidation(
            student.bairro))
        fieldInfoDict["cep"] = vars(FieldValidation.cepValidation(student.cep))
        fieldInfoDict["cidade"] = vars(FieldValidation.cidadeValidation(
            student.cidade))
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(student.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
        student.data_nascimento))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            student.email))
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(
            student.login))
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            student.nome))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            student.senha))
        fieldInfoDict["status"] = vars(FieldValidation.statusValidation(
            student.status))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            student.telefone))
        
        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict

assert isinstance(StudentRepository(session={}), student_repository.StudentRepository)