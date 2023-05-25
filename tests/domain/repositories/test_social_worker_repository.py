import sys
from pathlib import Path

# Adiciona o diretório "src" ao caminho de importação
sys.path.append(str(Path(__file__).resolve().parents[3]))

from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.domain.models.social_worker import SocialWorkerDB, SocialWorker
from src.infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from fastapi import HTTPException, status
from src.domain.models.social_worker import SocialWorker, SocialWorkerDB, SocialWorkerRequest, SocialWorkerResponse
from src.security import verify_password
from src.infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from sqlalchemy.orm import Session
from unittest.mock import patch
import pytest
from unittest.mock import MagicMock, patch
from unittest import mock


def test_find_all():
    # Arrange
    database = MagicMock(spec=Session)
    socialWorkerRepository = SocialWorkerRepository(database)
    expected_result = [SocialWorkerDB(), SocialWorkerDB()]
    database.query().all.return_value = expected_result

    # Act
    result = socialWorkerRepository.find_all()

    # Assert
    assert result == expected_result


def test_save_new_social_worker():
    # Arrange
    database = MagicMock(spec=Session)
    social_worker = SocialWorkerDB(login='john.doe', nome='John Doe', senha='123456', cpf='07497533150')
    database.query().filter().first.return_value = None
    socialWorkerRepository = SocialWorkerRepository(database)


    # Act
    result = socialWorkerRepository.save(social_worker)

    # Assert
    assert result == social_worker
    database.merge.assert_not_called()
    database.add.assert_called_once_with(social_worker)


def test_validateSocialWorker():
    # Arrange
    social_worker = SocialWorker(
        nome='John Doe',
        login='john.doe',
        senha='123456789',
        cpf='70761531653',
        dNascimento='2000-01-01',
        observacao='Observation',
        telefone='61986051611',
        email='john@example.com',
        administrador=False
    )

    database = MagicMock(spec=Session)
    result = SocialWorkerRepository(database).validateSocialWorker(social_worker)

    assert result['nome']['status'] is True
    assert result['login']['status'] is True
    assert result['senha']['status'] is True
    assert result['cpf']['status'] is True
    assert result['dNascimento']['status'] is True
    assert result['observacao']['status'] is True
    assert result['telefone']['status'] is True
    assert result['email']['status'] is True
    assert result['completeStatus'] is True


def test_invalidateSocialWorker():
    # Arrange
    social_worker = SocialWorker(
        nome='John Doe',
        login='john.doe',
        senha='16789',
        cpf='07497550', # cpf inválido
        dNascimento='2000-01-01',
        observacao='Observation',
        telefone='61986051611',
        email='john@example.com',
        administrador=False
    )
    
    database = MagicMock(spec=Session)
    result = SocialWorkerRepository(database).validateSocialWorker(social_worker)

    assert result['nome']['status'] is True
    assert result['login']['status'] is True
    assert result['senha']['status'] is False
    assert result['cpf']['status'] is False
    assert result['dNascimento']['status'] is True
    assert result['observacao']['status'] is True
    assert result['telefone']['status'] is True
    assert result['email']['status'] is True
    assert result['completeStatus'] is False


def test_invalidateSocialWorker_2():
    # Arrange
    social_worker = SocialWorker(
        nome='John Doe',
        login='john.doe',
        senha='16765465465489',
        cpf='70761531653', 
        dNascimento='2000-01-01',
        observacao='Observation',
        telefone='619811',
        email='john@example.com',
        administrador=False
    )
    
    database = MagicMock(spec=Session)
    result = SocialWorkerRepository(database).validateSocialWorker(social_worker)

    assert result['nome']['status'] is True
    assert result['login']['status'] is True
    assert result['senha']['status'] is True
    assert result['cpf']['status'] is True
    assert result['dNascimento']['status'] is True
    assert result['observacao']['status'] is True
    assert result['telefone']['status'] is False
    assert result['email']['status'] is True
    assert result['completeStatus'] is False

@mock.patch("infrastructure.repositories.social_worker_repository.SocialWorkerRepository")
def test_find_all(mock_repository):
    # Criação do mock do repositório
    mock_repository_instance = mock_repository.return_value
    mock_repository_instance.find_all.return_value = [
        SocialWorkerResponse(
            nome="John Doe",
            login="john.doe",
            senha="123456789",
            cpf="07497533150",
            dNascimento="2000-01-01",
            observacao="Observation",
            email="john.doe@example.com",
            telefone="12345678912",
            administrador=True
        )
    ]

    social_workers = mock_repository_instance.find_all()


    mock_repository_instance.find_all.assert_called_once()

    # Verifica o resultado retornado pela função
    assert len(social_workers) == 1
    assert social_workers[0].nome == "John Doe"
    assert social_workers[0].login == "john.doe"
    assert social_workers[0].senha == "123456789"
    assert social_workers[0].cpf == "07497533150"
    assert social_workers[0].dNascimento == "2000-01-01"
    assert social_workers[0].observacao == "Observation"
    assert social_workers[0].email == "john.doe@example.com"
    assert social_workers[0].telefone == "12345678912"
    assert social_workers[0].administrador is True