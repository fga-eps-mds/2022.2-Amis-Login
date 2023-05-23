from sqlalchemy.orm import Session
from ..models.teacher import Teacher
from typing import List
from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response
from ...infrastructure.repositories.field_repository import FieldValidation

class TeacherRepository:

    @staticmethod
    def save_teacher(db: Session, teacher: Teacher) -> Teacher:
        if TeacherRepository.exists_by_codigo_teacher(db, Teacher.codigo):
            db.merge(teacher)
        else:
            db.add(teacher)
        db.commit()
        return teacher

    @staticmethod
    def find_all_teacher(db: Session) -> List[Teacher]:
        return db.query(Teacher).all()
    
    @staticmethod
    def find_by_codigo_teacher(db : Session, codigo : str) -> Teacher:
        return db.query(Teacher).filter(Teacher.codigo == codigo).first()
    
    @staticmethod
    def exists_by_codigo_teacher(database: Session, codigo: str) -> bool:
        '''Função que verifica se o login dado existe na DB'''
        return database.query(Teacher).filter(Teacher.codigo == codigo).first() is \
            not None




    @staticmethod
    def validate_teacher(teacher : Teacher) -> dict:

        fieldInfoDict = {}
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(teacher.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
        teacher.data_nascimento))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            teacher.email))
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            teacher.nome))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            teacher.telefone))
        
        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict
        