import pytest
from fastapi import HTTPException
from unittest.mock import Mock, MagicMock
from domain.repositories.supervisor_repository import SupervisorRepository
from domain.repositories.tokens_repository import TokensRepositoryBaseModel
from domain.models.supervisor import Supervisor, SupervisorBase
from security import verify_password
from application.supervisor_service import SupervisorService
import unittest


@pytest.fixture
def supervisor_repository():
    return Mock(spec=SupervisorRepository)


@pytest.fixture
def tokens_repository():
    return Mock(spec=TokensRepositoryBaseModel)


@pytest.fixture
def supervisor_repository_mock():
    return MagicMock()


@pytest.fixture
def tokens_repository_mock():
    return MagicMock()


@pytest.fixture
def supervisor_service(supervisor_repository, tokens_repository):
    return SupervisorService(supervisor_repository, tokens_repository)


def test_login_invalid_credentials(
    supervisor_service, supervisor_repository, tokens_repository
):
    supervisor_repository.find_by_login_supervisor.return_value = None

    with pytest.raises(HTTPException) as exc:
        supervisor_service.login("test", "password")

    assert exc.value.status_code == 401
    assert exc.value.detail == "Email ou nome de usuário incorretos"
    supervisor_repository.find_by_login_supervisor.assert_called_once_with("test")


def test_verify_token(supervisor_service, tokens_repository):
    token = "example_token"
    user_login = "example_user_login"
    supervisor = SupervisorBase(
        login="example_login",
        nome="example_nome",
        senha="example_senha",
        data_nascimento="example_data_nascimento",
        cpf="example_cpf",
        telefone="example_telefone",
        email="example_email",
    )

    tokens_repository.verifyToken.return_value = user_login
    supervisor_service.__supervisorRepository__.find_by_login_supervisor.return_value = (
        supervisor
    )

    result = supervisor_service.verifyToken(token)

    assert result == supervisor
    tokens_repository.verifyToken.assert_called_once_with(token=token)
    supervisor_service.__supervisorRepository__.find_by_login_supervisor.assert_called_once_with(
        user_login
    )


def test_refresh_session_valid_token(supervisor_service, tokens_repository):
    tokens_repository.verifyToken.return_value = True
    tokens_repository.refreshToken.return_value = (
        "new_user_token",
        "new_refresh_token",
    )

    result = supervisor_service.refreshSession("refresh_token")

    assert result == ("new_user_token", "new_refresh_token")
    tokens_repository.verifyToken.assert_called_once_with(token="refresh_token")
    tokens_repository.refreshToken.assert_called_once_with(
        refresh_token="refresh_token"
    )


def test_refresh_session_invalid_token(supervisor_service, tokens_repository):
    tokens_repository.verifyToken.return_value = False

    result = supervisor_service.refreshSession("refresh_token")

    assert result is None
    tokens_repository.verifyToken.assert_called_once_with(token="refresh_token")


def test_find_by_login(supervisor_service, supervisor_repository):
    supervisor_repository.find_by_login_supervisor.return_value = Supervisor(
        login="test"
    )

    result = supervisor_service.find_by_login("test")

    assert result.login == "test"
    supervisor_repository.find_by_login_supervisor.assert_called_once_with("test")


def test_find_all(supervisor_service, supervisor_repository):
    supervisor1 = Supervisor(
        login="test1",
        nome="Nome do Supervisor 1",
        senha="senha123",
        data_nascimento="01/01/1990",
        cpf="12345678901",
        telefone="1234567890",
        email="supervisor1@example.com",
    )
    supervisor2 = Supervisor(
        login="test2",
        nome="Nome do Supervisor 2",
        senha="senha456",
        data_nascimento="02/02/1995",
        cpf="98765432109",
        telefone="9876543210",
        email="supervisor2@example.com",
    )
    supervisor_repository.find_all_supervisor.return_value = [supervisor1, supervisor2]

    result = supervisor_service.find_all()

    expected_result = [
        {
            "login": supervisor.login,
            "nome": supervisor.nome,
            "senha": supervisor.senha,
            "data_nascimento": supervisor.data_nascimento,
            "cpf": supervisor.cpf,
            "telefone": supervisor.telefone,
            "email": supervisor.email,
        }
        for supervisor in [supervisor1, supervisor2]
    ]

    result_dicts = [
        {k: v for k, v in vars(supervisor).items() if k != "_sa_instance_state"}
        for supervisor in result
    ]

    assert result_dicts == expected_result
    supervisor_repository.find_all_supervisor.assert_called_once()


def test_exists_by_login(supervisor_service, supervisor_repository):
    supervisor_repository.find_by_login_supervisor.return_value = Supervisor(
        login="test"
    )

    result = supervisor_service.exists_by_login("test")

    assert result is True
    supervisor_repository.find_by_login_supervisor.assert_called_once_with("test")


def test_exists_by_login_nonexistent(supervisor_service, supervisor_repository):
    supervisor_repository.find_by_login_supervisor.return_value = None

    result = supervisor_service.exists_by_login("test")

    assert result is False
    supervisor_repository.find_by_login_supervisor.assert_called_once_with("test")


def test_delete_refresh_token(tokens_repository_mock):
    # Creating an instance of SocialWorkerService with mocked objects
    service = SupervisorService(
        supervisorRepository=MagicMock(),
        tokensRepository=tokens_repository_mock,
    )

    # Calling the delete_refresh_token method
    result = service.delete_refresh_token(refresh_token="test_refresh_token")

    # Assertions
    assert result is None


def test_save(supervisor_service, supervisor_repository):
    supervisor = Supervisor(login="test")
    supervisor_repository.save_supervisor.return_value = supervisor

    result = supervisor_service.save(supervisor)

    assert result == supervisor
    supervisor_repository.save_supervisor.assert_called_once_with(supervisor)


def test_delete_by_login(supervisor_service, supervisor_repository):
    supervisor_service.delete_by_login("test")
    supervisor_repository.delete_by_login_supervisor.assert_called_once_with("test")


def test_validate_supervisor(supervisor_service):
    supervisor = Supervisor(
        login="testtest",
        nome="Testtest",
        data_nascimento="2000-01-01",
        cpf="105664830174",
        telefone="61998116543",
        email="tesasdat@example.com",
        senha="password123",
    )

    result = supervisor_service.validate_supervisor(supervisor)

    expected_result = {
        "cpf": {"status": False, "detail": "CPF muito grande"},
        "dNascimento": {"status": True, "detail": "Data de nascimento válida"},
        "email": {"status": True, "detail": "Email válido"},
        "login": {"status": True, "detail": "Login válido"},
        "nome": {"status": True, "detail": "Nome válido"},
        "senha": {"status": True, "detail": "Senha válida"},
        "telefone": {"status": True, "detail": "Telefone válido"},
        "completeStatus": False,
    }

    assert result == expected_result
