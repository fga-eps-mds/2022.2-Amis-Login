from sqlalchemy.orm import Session
from ..models.student import Student
from typing import List
from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response


class StudentRepository:
    
    @staticmethod
    def save_student(db: Session, student: Student) -> Student:
        if student.login:
            db.merge(student)
        else:
            db.add(student)
        db.commit()
        return student

    @staticmethod
    def find_all_student(db: Session) -> List[Student]:
        return db.query(Student).all()
    
    @staticmethod
    def find_by_login_student(db : Session, login : str) -> Student:
        return db.query(Student).filter(Student.login == login).first()
    
    @staticmethod
    def exists_by_cpf_student(db: Session, cpf: str) -> bool:
        return db.query(Student).filter(Student.cpf == cpf).first() is not None 

    @staticmethod
    def delete_by_login_student(db: Session, login: str) -> None:
        student = db.query(Student).filter(Student.login == login).first()
        if student is not None:
            db.delete(student)
            db.commit()

    @staticmethod
    def update_by_login(db: Session, student_request: Student) -> Student:

        student = StudentRepository.find_by_login_student(db, student_request.login) 
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
        
       
 
        StudentRepository.save_student(db, student)
        return student
