from domain.models.teacher import TeacherDB, Teacher
from domain.repositories import teacher_repository
from .field_repository import FieldValidation
from sqlalchemy.orm import Session
from typing import Callable

class TeacherRepository:

    database: Callable[[], Session]

    def __init__(self, session = Callable[[], Session]):
        self.database = session

    
    def find_all(self) -> list[TeacherDB]:
        session = self.database()
        res = session.query(TeacherDB).all()
        session.close()
        return res
    

    def find_by_login(self, login : str) -> TeacherDB | None:
        session = self.database()
        return session.query(TeacherDB).filter(TeacherDB.login == login).first()


    def save(self, teacherSent : TeacherDB) -> TeacherDB:
        session = self.database()
        if self.find_by_login(teacherSent.login):
            session.merge(teacherSent)
        else:
            session.add(teacherSent)

        session.commit()
        session.expunge_all()
        session.close()
        return teacherSent
    

    def delete_by_login(self, login: str) -> None:
        session = self.database()
        teacher_object = session.query(TeacherDB).filter(
            TeacherDB.login == login).first()

        if teacher_object is not None:
            session.delete(teacher_object)
            session.commit()

        session.close()

    
    def validate_teacher(self, teacher : Teacher) -> dict:

        fieldInfoDict = {}
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(teacher.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
        teacher.data_nascimento))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            teacher.email))
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(teacher.login))
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            teacher.nome))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            teacher.senha))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            teacher.telefone))
        
        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict
        
    
assert isinstance(TeacherRepository(
    {}), teacher_repository.TeacherRepositoryBaseModel)