from domain.models.student import Student
from infrastructure.repositories.student_repository import StudentRepository
from domain.models.student import Status
from fastapi import HTTPException, status
import pytest


# Test data
test_student_data = {
    "bairro": "Test Bairro",
    "cep": "12345678",
    "cidade": "Test City",
    "cpf": "17553041025",
    "data_nascimento": "2000-01-01",
    "deficiencia": False,
    "descricao_endereco": "Test Address",
    "email": "test@example.com",
    "login": "testuser",
    "nome": "Test User",
    "senha": "testpassword",
    "status": Status.PRODUCAO,
    "telefone": "12234567890"
}

# Mocking Session class for testing


class MockSession:
    def merge(self, student):
        pass

    def add(self, student):
        pass

    def commit(self):
        pass

    def query(self, model):
        return self

    def all(self):
        return []

    def filter(self, condition):
        return self

    def first(self):
        return None

    def delete(self, student):
        pass


def mock_db_session():
    return MockSession()


def test_save_student():
    student_repo = StudentRepository(mock_db_session)
    student = Student(**test_student_data)

    result = student_repo.save_student(student)

    assert result == student


def test_find_all_student():
    student_repo = StudentRepository(mock_db_session)

    result = student_repo.find_all_student()

    assert result == []


def test_find_by_login_student():
    student_repo = StudentRepository(mock_db_session)

    result = student_repo.find_by_login_student("testuser")

    assert result is None


def test_exists_by_cpf_student():
    student_repo = StudentRepository(mock_db_session)

    result = student_repo.exists_by_cpf_student("12345678901")

    assert result is False


def test_delete_by_login_student():
    student_repo = StudentRepository(mock_db_session)

    student_repo.delete_by_login_student("testuser")

    # No assertion, just making sure the function runs without errors


def test_update_by_login():
    student_repo = StudentRepository(mock_db_session)
    student = Student(**test_student_data)

    with pytest.raises(HTTPException) as exc:
        student_repo.update_by_login(student)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert str(exc.value.detail) == "student não encontrado"


def test_save_student_existing_login():
    student_repo = StudentRepository(mock_db_session)
    student = Student(**test_student_data)
    student.login = "existinguser"

    result = student_repo.save_student(student)

    assert result == student


def test_find_by_login_student_existing_login():
    student_repo = StudentRepository(mock_db_session)
    existing_student = Student(**test_student_data)
    existing_student.login = "existinguser"
    mock_db_session().first = lambda: existing_student

    result = student_repo.find_by_login_student("existinguser")

    assert result == existing_student


def test_exists_by_cpf_student_existing_cpf():
    student_repo = StudentRepository(mock_db_session)
    existing_student = Student(**test_student_data)
    existing_student.cpf = "12345678901"
    mock_db_session.first = lambda: existing_student

    result = student_repo.exists_by_cpf_student("12345678901")

    assert result is True


def test_delete_by_login_student_existing_login():
    student_repo = StudentRepository(mock_db_session)
    existing_student = Student(**test_student_data)
    existing_student.login = "existinguser"
    mock_db_session.first = lambda: existing_student

    student_repo.delete_by_login_student("existinguser")

    # No assertion, just making sure the function runs without errors


def test_update_by_login_existing_login():
    student_repo = StudentRepository(mock_db_session)
    existing_student = Student(**test_student_data)
    existing_student.login = "existinguser"
    mock_db_session.first = lambda: existing_student

    result = student_repo.update_by_login(existing_student)

    assert result == existing_student


def test_save_student_without_login():
    student_repo = StudentRepository(mock_db_session)
    student = Student(**test_student_data)
    student.login = None

    result = student_repo.save_student(student)

    assert result == student


def test_find_by_login_student_nonexistent_login():
    student_repo = StudentRepository(mock_db_session)
    mock_db_session.first = lambda: None

    result = student_repo.find_by_login_student("nonexistentuser")

    assert result is None


def test_exists_by_cpf_student_nonexistent_cpf():
    student_repo = StudentRepository(mock_db_session)
    mock_db_session.first = lambda: None

    result = student_repo.exists_by_cpf_student("99999999999")

    assert result is False


def test_update_by_login_nonexistent_login():
    student_repo = StudentRepository(mock_db_session)
    mock_db_session.first = lambda: None

    with pytest.raises(HTTPException) as exc:
        student_repo.update_by_login(
            student_request=Student(**test_student_data))

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert str(exc.value.detail) == "student não encontrado"


def test_validate_student_complete_fields():
    student_repo = StudentRepository(mock_db_session)
    student = Student(**test_student_data)

    result = student_repo.validate_student(student)

    assert result["completeStatus"] is True


def test_validate_student_incomplete_fields():
    student_repo = StudentRepository(mock_db_session)
    student_data = test_student_data.copy()
    student_data["nome"] = ""
    student_data["cpf"] = ""
    student = Student(**student_data)

    result = student_repo.validate_student(student)

    assert result["completeStatus"] is False
    assert result["nome"]["status"] is False
    assert result["cpf"]["status"] is False
