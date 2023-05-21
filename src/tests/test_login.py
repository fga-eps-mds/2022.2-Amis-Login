from fastapi.testclient import TestClient
import pytest
import coverage
import requests


@pytest.fixture
def client():
    from ..main import app
    with TestClient(app) as client:
        yield client


def test_sucessful_login(client):
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'username': 'test',
        'password': 'test',
    }

    response = requests.post('http://localhost:9090/login/', headers=headers, data=data)

    assert response.status_code == 200


def test_failed_login(client):
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'username': 'unregistered',
        'password': 'unregistered',
    }

    response = requests.post('http://localhost:9090/login/', headers=headers, data=data)

    assert response.status_code == 403