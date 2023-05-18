from sqlalchemy.orm import Session
from ..model.model import Aluno
from typing import List
from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response


class AlunoRepository:
    
    @staticmethod
    def save_aluno(db: Session, aluno: Aluno) -> Aluno:
        if aluno.login:
            db.merge(aluno)
        else:
            db.add(aluno)
        db.commit()
        return aluno

    @staticmethod
    def find_all_aluno(db: Session) -> List[Aluno]:
        return db.query(Aluno).all()
    
    @staticmethod
    def find_by_login_aluno(db : Session, login : str) -> Aluno:
        return db.query(Aluno).filter(Aluno.login == login).first()
    
    @staticmethod
    def exists_by_cpf_aluno(db: Session, cpf: str) -> bool:
        return db.query(Aluno).filter(Aluno.cpf == cpf).first() is not None 

    @staticmethod
    def delete_by_login_aluno(db: Session, login: str) -> None:
        aluno = db.query(Aluno).filter(Aluno.login == login).first()
        if aluno is not None:
            db.delete(aluno)
            db.commit()

    @staticmethod
    def update_by_login(db: Session, aluno_request: Aluno) -> Aluno:

        aluno = AlunoRepository.find_by_login_aluno(db, aluno_request.login) 
        if not aluno:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado"
        )

        aluno.bairro = aluno_request.bairro
        aluno.cep = aluno_request.cep
        aluno.cidade = aluno_request.cidade
        aluno.cpf = aluno_request.cpf
        aluno.data_nascimento = aluno_request.data_nascimento
        aluno.deficiencia = aluno_request.deficiencia
        aluno.descricao_endereco = aluno_request.descricao_endereco
        aluno.email = aluno_request.email
        aluno.nome = aluno_request.nome
        aluno.senha = aluno_request.senha
        aluno.status = aluno_request.status
        aluno.telefone = aluno_request.telefone
        
       
 
        AlunoRepository.save_aluno(db, aluno)
        return aluno
