import sys
from pathlib import Path
import pytest

# Adiciona o diretório "src" ao caminho de importação
sys.path.append(str(Path(__file__).resolve().parents[3]))

from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.domain.models.social_worker import SocialWorkerDB, SocialWorker
from src.infrastructure.repositories.field_repository import FieldValidation
from src.domain.repositories.social_worker_repository import SocialWorkerRepository


def test_find_all():
    # Arrange
    database = MagicMock(spec=Session)
    expected_result = [SocialWorkerDB(), SocialWorkerDB()]
    database.query().all.return_value = expected_result

    # Act
    result = SocialWorkerRepository.find_all(database)

    # Assert
    assert result == expected_result


def test_save_new_social_worker():
    # Arrange
    database = MagicMock(spec=Session)
    social_worker = SocialWorkerDB(login='john.doe', nome='John Doe', senha='123456')
    database.query().filter().first.return_value = None

    # Act
    result = SocialWorkerRepository.save(database, social_worker)

    # Assert
    assert result == social_worker
    database.merge.assert_not_called()
    database.add.assert_called_once_with(social_worker)
