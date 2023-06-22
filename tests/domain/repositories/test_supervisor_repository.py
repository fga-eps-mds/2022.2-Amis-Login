import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from domain.models.supervisor import Supervisor, SupervisorRequest, SupervisorResponse
from infrastructure.repositories.supervisor_repository import SupervisorRepository


def generate_session():
    return MagicMock(spec=Session)


def test_save_supervisor():
    # Arrange
    database = generate_session
    test_session = database()

    supervisor = SupervisorRequest(
        login="john.doe",
        nome="John Doe",
        senha="123456",
        data_nascimento="2000-01-01",
        cpf="07497533150",
        telefone="1234567890",
        email="john@example.com",
    )
    test_session.query().filter().first.return_value = None
    supervisorRepository = SupervisorRepository(database)

    # Act
    result = supervisorRepository.save_supervisor(supervisor)

    # Assert
    assert result.login == supervisor.login
    assert result.nome == supervisor.nome
    assert result.senha == supervisor.senha
    assert result.data_nascimento == supervisor.data_nascimento
    assert result.cpf == supervisor.cpf
    assert result.telefone == supervisor.telefone
    assert result.email == supervisor.email

    test_session.close()


def test_find_by_login_supervisor():
    # Arrange
    database = generate_session()
    supervisorRepository = SupervisorRepository(database)
    login = "john.doe"
    expected_result = Supervisor(
        login=login,
        nome="John Doe",
        data_nascimento="2000-01-01",
        cpf="07497533150",
        telefone="1234567890",
        email="john@example.com",
        senha="senha",
    )
    # Adjust the mock setup to return the expected result
    database().query().filter().first.return_value = expected_result

    # Act
    result = supervisorRepository.find_by_login_supervisor(login)

    # Assert
    assert result == expected_result


def test_exists_by_cpf_supervisor():
    # Arrange
    database = generate_session
    supervisorRepository = SupervisorRepository(database)
    cpf = "12345678901"
    database().query().filter().first.return_value = Supervisor()

    # Act
    result = supervisorRepository.exists_by_cpf_supervisor(cpf)

    # Assert
    assert result is True


def test_update_by_login():
    # Arrange
    database = generate_session
    test_session = database()
    supervisorRepository = SupervisorRepository(database)
