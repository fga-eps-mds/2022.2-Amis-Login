from sqlalchemy.orm import Session
from ..model.model import Aluno, Telefone
from typing import List
from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Response



class AlunoRepository:
    
    @staticmethod
    def save_aluno(db: Session, aluno: Aluno) -> Aluno:
        if aluno.cpf:
            db.merge(aluno)
        else:
            db.add(aluno)
        db.commit()
        return aluno

    @staticmethod
    def find_all_aluno(db: Session) -> List[Aluno]:
        return db.query(Aluno).all()
    
    @staticmethod
    def find_by_cpf_aluno(db : Session, cpf : str) -> Aluno:
        return db.query(Aluno).filter(Aluno.cpf == cpf).first()

    @staticmethod
    def exists_by_cpf_aluno(db: Session, cpf: str) -> bool:
        return db.query(Aluno).filter(Aluno.cpf == cpf).first() is not None

    @staticmethod
    def delete_by_cpf_aluno(db: Session, cpf: str) -> None:
        aluno = db.query(Aluno).filter(Aluno.cpf == cpf).first()
        if aluno is not None:
            db.delete(aluno)
            db.commit()

    @staticmethod
    def update_by_cpf(db: Session, aluno_request: Aluno) -> Aluno:

        aluno = AlunoRepository.find_by_cpf_aluno(db, aluno_request.cpf) 
        if not aluno:
            raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado"
        )

        aluno.nome = aluno_request.nome
        aluno.nome_social = aluno_request.nome_social
        aluno.data_nascimento = aluno_request.data_nascimento
        aluno.deficiencia = aluno_request.deficiencia
        aluno.rg = aluno_request.rg
        aluno.cidade = aluno_request.cidade
        aluno.bairro = aluno_request.bairro
        aluno.cep = aluno_request.cep
        aluno.descricao_endereco = aluno_request.descricao_endereco
        aluno.senha = aluno_request.senha
 
        AlunoRepository.save_aluno(db, aluno)
        return aluno

class TelefoneRepository:
    @staticmethod
    def find_all_telefone(db: Session) -> List[Telefone]:
        return db.query(Telefone).all()

    @staticmethod
    def save_telefone(db: Session, telefone: Telefone) -> Telefone:
        if telefone.id:
            db.merge(telefone)
        else:
            db.add(telefone)
        db.commit()
        return telefone

    @staticmethod
    def find_by_id_telefone(db: Session, id: int) -> Telefone:
        return db.query(Telefone).filter(Telefone.id_telefone == id).first()

    @staticmethod
    def exists_by_id_telefone(db: Session, id: int) -> bool:
        return db.query(Telefone).filter(Telefone.id == id).first() is not None

    @staticmethod
    def delete_by_id_telefone(db: Session, id: int) -> None:
        telefone = db.query(Telefone).filter(Telefone.id == id).first()
        if telefone is not None:
            db.delete(telefone)
            db.commit()
