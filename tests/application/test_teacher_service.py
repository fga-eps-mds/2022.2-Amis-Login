import pytest
from unittest.mock import MagicMock, Mock, patch
from application.teacher_service import TeacherService
from domain.models.teacher import Teacher
from fastapi.testclient import TestClient
import requests

@pytest.fixture
def teacher_repository_mock():
    return MagicMock()

@pytest.fixture
def tokens_repository_mock():
    return MagicMock()

@pytest.fixture
def client():
    from main import app
    with TestClient(app) as client:
        yield client

# def test_sucessful_login(client):
#     headers = {
#         'accept': 'application/json',
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }

#     data = {
#         'username': 'test',
#         'password': 'test',
#     }

#     response = requests.post('http://localhost:9090/login/', headers=headers, data=data)

#     assert response.status_code == 200


# def test_failed_login(client):
#     username = os.environ.get('TEST_USERNAME')
#     password = os.environ.get('TEST_PASSWORD')

#     headers = {
#         'accept': 'application/json',
#         'Content-Type': 'application/x-www-form-urlencoded',
#     }
#     data = {
#         'username': username,
#         'password': password,
#     }
#     response = requests.post('http://localhost:9090/login/', headers=headers, data=data)
#     assert response.status_code == 403

# def test_verify_token(teacher_repository_mock, tokens_repository_mock):
#     # Mocking the necessary objects
#     tokens_repository_mock.verifyToken.return_value = "testuser"
#     teacher = Teacher(
#         nome="John Doe",
#         login="testuser",
#         senha="password",
#         cpf="1234567890",
#         data_nascimento="1994-02-09",
#         cursos="Culinária",
#         email="email@test.com",
#         telefone="61921432134"
#     )
#     teacher_repository_mock.find_by_login.return_value = teacher

#     # Creating an instance of TeacherService with mocked objects
#     service = TeacherService(
#         teachersRepository=teacher_repository_mock,
#         tokensRepository=tokens_repository_mock
#     )

#     # Calling the verifyToken method
#     returned_teacher = service.verifyToken(token="test_token")

#     # Assertions
#     assert returned_teacher == teacher
#     tokens_repository_mock.verifyToken.assert_called_once_with(token="test_token")
#     teacher_repository_mock.find_by_login.assert_called_once_with("testuser")

def test_refresh_session(tokens_repository_mock):
    # Mocking the necessary objects
    tokens_repository_mock.verifyToken.return_value = True
    tokens_repository_mock.refreshToken.return_value = ("new_user_token", "new_refresh_token")

    # Creating an instance of TeacherService with mocked objects
    service = TeacherService(
        teachersRepository=MagicMock(),
        tokensRepository=tokens_repository_mock
    )

    # Calling the refreshSession method
    result = service.refreshSession(refresh_token="test_refresh_token")

    # Assertions
    assert result == ("new_user_token", "new_refresh_token")
    tokens_repository_mock.verifyToken.assert_called_once_with(token="test_refresh_token")
    tokens_repository_mock.refreshToken.assert_called_once_with(refresh_token="test_refresh_token")
    
def test_failed_refresh_session_invalid_token(tokens_repository_mock):
    # Mocking the necessary objects
    tokens_repository_mock.verifyToken.return_value = False

    # Creating an instance of TeacherService with mocked objects
    service = TeacherService(
        teachersRepository=MagicMock(),
        tokensRepository=tokens_repository_mock
    )

    # Calling the refreshSession method
    result = service.refreshSession(refresh_token="invalid_token")

    # Assertions
    assert result is None

def test_delete_refresh_token(tokens_repository_mock):
    # Creating an instance of TeacherService with mocked objects
    service = TeacherService(
        teachersRepository=MagicMock(),
        tokensRepository=tokens_repository_mock
    )

    # Calling the delete_refresh_token method
    result = service.delete_refresh_token(refresh_token="test_refresh_token")

    # Assertions
    assert result is None