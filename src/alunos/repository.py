from sqlalchemy.orm import Session
from ..model.model import Aluno, Telefone

class AlunoRepository:
    
    @staticmethod
    def save_aluno(db: Session, aluno: Aluno) -> Aluno:
        if aluno.id_aluno:
            db.merge(aluno)
        else:
            db.add(aluno)
        db.commit()
        return aluno

    @staticmethod
    def find_all_aluno(db: Session) -> list[Aluno]:
        return db.query(Aluno).all()
    
    @staticmethod
    def find_by_id_aluno(db: Session, id: int) -> Aluno:
        return db.query(Aluno).filter(Aluno.id_aluno == id).first()
    
    @staticmethod
    def find_by_cpf_aluno(db : Session, cpf : str) -> Aluno:
        return db.query(Aluno).filter(Aluno.cpf == cpf).first()

    @staticmethod
    def exists_by_id_aluno(db: Session, id: int) -> bool:
        return db.query(Aluno).filter(Aluno.id_aluno == id).first() is not None
    
    @staticmethod
    def exists_by_cpf_aluno(db: Session, cpf: str) -> bool:
        return db.query(Aluno).filter(Aluno.cpf == cpf).first() is not None

    @staticmethod
    def delete_by_id_aluno(db: Session, id: int) -> None:
        aluno = db.query(Aluno).filter(Aluno.id_aluno == id).first()
        if aluno is not None:
            db.delete(aluno)
            db.commit()

    @staticmethod
    def delete_by_cpf_aluno(db: Session, cpf: str) -> None:
        aluno = db.query(Aluno).filter(Aluno.cpf == cpf).first()
        if aluno is not None:
            db.delete(aluno)
            db.commit()

    @staticmethod
    def update_by_cpf(db: Session, aluno: Aluno) -> Aluno:
        if aluno.cpf:
            db.merge(aluno)
        else:
            db.add(aluno)
        db.commit()
        return aluno

class TelefoneRepository:
    @staticmethod
    def find_all_telefone(db: Session) -> list[Telefone]:
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
        return db.query(Telefone).filter(Telefone.id == id).first()

    @staticmethod
    def exists_by_id_telefone(db: Session, id: int) -> bool:
        return db.query(Telefone).filter(Telefone.id == id).first() is not None

    @staticmethod
    def delete_by_id_telefone(db: Session, id: int) -> None:
        telefone = db.query(Telefone).filter(Telefone.id == id).first()
        if telefone is not None:
            db.delete(telefone)
            db.commit()
