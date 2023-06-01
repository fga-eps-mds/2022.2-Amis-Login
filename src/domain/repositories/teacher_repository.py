from ..models.teacher import TeacherDB, Teacher
from typing import Protocol, runtime_checkable

@runtime_checkable
class TeacherRepositoryBaseModel(Protocol):

    def find_all(self) -> list[TeacherDB]:
        '''Função para fazer uma query de todas as Teacher da DB'''
        ...


    def find_by_login(self, login: str) -> TeacherDB | None:
        '''Função para fazer uma query por login de um objeto Teacher na DB'''
        ...

    def save(self, teacherSent: TeacherDB) -> TeacherDB:
        '''Função para salvar um objeto assistente na DB'''
        ...

    def delete_by_login(self, login: str) -> None:
        '''Função para excluir um objeto assistente da DB dado o login'''
        ...

    def validate_teacher(self, teacher: Teacher) -> dict:
        '''Função para validar os campos de um objeto Teacher'''
        ...