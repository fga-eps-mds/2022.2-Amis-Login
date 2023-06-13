from unittest import mock
from unittest.mock import MagicMock, patch
import pytest
from security import verify_password
from domain.models.teacher import Teacher, TeacherRequest, TeacherResponse
from fastapi import HTTPException, status
from infrastructure.repositories.teacher_repository import TeacherRepository
from sqlalchemy.orm import Session
import sys
from pathlib import Path

# Adiciona o diretório "src" ao caminho de importação
sys.path.append(str(Path(__file__).resolve().parents[3]))


def generate_session():
    return MagicMock(spec=Session)


def test_find_all():
    # Arrange
    database = generate_session()
    teacherRepository = TeacherRepository(database)
    expected_result = [Teacher(), Teacher()]
    database.query().all.return_value = expected_result

    # Act
    result = teacherRepository.find_all()

    # Assert
    assert result == expected_result


def test_save_new_teacher():
    # Arrange
    database = generate_session()
    test_session = database

    teacher = Teacher(
        cpf='70761531653',
        habilidades='Confeitaria',
        data_nascimento='2000-01-01',
        email='john@example.com',
        login='john.doe',
        nome='John Doe',
        senha='123456789',
        telefone='61986051611'
    )
    test_session.query().filter().first.return_value = None
    teacherRepository = TeacherRepository(database)

    # Act
    result = teacherRepository.save(teacher)

    # Assert
    assert result == teacher

    test_session.close()


def test_validateTeacher():
    # Arrange
    teacher = Teacher(
        cpf='70761531653',
        habilidades='Confeitaria',
        data_nascimento='2000-01-01',
        email='john@example.com',
        login='john.doe',
        nome='John Doe',
        senha='123456789',
        telefone='61986051611'
    )

    database = generate_session()
    result = TeacherRepository(database).validate_teacher(teacher)

    assert result['cpf']['status'] is True
    assert result['dNascimento']['status'] is True
    assert result['email']['status'] is True
    assert result['login']['status'] is True
    assert result['nome']['status'] is True
    assert result['senha']['status'] is True
    assert result['telefone']['status'] is True
    assert result['completeStatus'] is True


def test_invalidateTeacher():
    # Arrange
    teacher = Teacher(
        cpf='07497550',
        habilidades='Confeitaria',
        data_nascimento='2000-01-01',
        email='john@example.com',
        login='john.doe',
        nome='John Doe',
        senha='123456789',
        telefone='61986051611'
    )

    database = generate_session()
    result = TeacherRepository(database).validate_teacher(teacher)

    assert result['cpf']['status'] is False
    assert result['dNascimento']['status'] is True
    assert result['email']['status'] is True
    assert result['login']['status'] is True
    assert result['nome']['status'] is True
    assert result['senha']['status'] is True
    assert result['telefone']['status'] is True
    assert result['completeStatus'] is False


def test_invalidateTeacher_2():
    # Arrange
    teacher = Teacher(
        cpf='07497550',
        habilidades='Confeitaria',
        data_nascimento='2000-01-01',
        email='john@example.com',
        login='john.doe',
        nome='John Doe',
        senha='123456789',
        telefone='619811'
    )

    database = generate_session()
    result = TeacherRepository(database).validate_teacher(teacher)

    assert result['cpf']['status'] is False
    assert result['dNascimento']['status'] is True
    assert result['email']['status'] is True
    assert result['login']['status'] is True
    assert result['nome']['status'] is True
    assert result['senha']['status'] is True
    assert result['telefone']['status'] is False
    assert result['completeStatus'] is False


@mock.patch("infrastructure.repositories.teacher_repository.TeacherRepository")
def test_find_all(mock_repository):
    # Criação do mock do repositório
    mock_repository_instance = mock_repository.return_value
    mock_repository_instance.find_all.return_value = [
        TeacherResponse(
            cpf='70761531653',
            habilidades='Confeitaria',
            data_nascimento='2000-01-01',
            email='john@example.com',
            login='john.doe',
            nome='John Doe',
            senha='123456789',
            telefone='61986051611'
        )
    ]

    teacherRepository = mock_repository_instance
    teacher = teacherRepository.find_all()

    mock_repository_instance.find_all.assert_called_once()

    # Verifica o resultado retornado pela função
    assert len(teacher) == 1
    assert teacher[0].cpf == "70761531653"
    assert teacher[0].data_nascimento == "2000-01-01"
    assert teacher[0].email == "john@example.com"
    assert teacher[0].login == "john.doe"
    assert teacher[0].nome == "John Doe"
    assert teacher[0].senha == "123456789"
    assert teacher[0].telefone == "61986051611"
