import pytest
from httpx import AsyncClient
from fastapi import status

GLOBAL_RESPONSE = []
HTTPS_TEACHER = "http://localhost:9090"

# CREATE
@pytest.mark.asyncio
async def test_create_teacher():
    data = {        
        "cpf": "17553041025",
        "habilidades": "Test Address",
        "data_nascimento": "2000-01-01",
        "email": "testamis@gmail.com",
        "login": "amisteste2",
        "nome": "amisteste1",
        "senha": "testpassword",
        "telefone": "12234567890"
    }
    async with AsyncClient(base_url=HTTPS_TEACHER, timeout=30.0) as async_client:
        response = await async_client.post("/teacher/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

# GET ALL
@pytest.mark.asyncio
async def test_read_all_teacher():
    async with AsyncClient(base_url=HTTPS_TEACHER, timeout=30.0) as async_client:
        response = await async_client.get("/teacher/")
    assert response.status_code == status.HTTP_200_OK


# FIND BY LOGIN
@pytest.mark.asyncio
async def test_find_by_login_teacher():
    login = "amisteste2"
    async with AsyncClient(base_url=HTTPS_TEACHER, timeout=30.0) as async_client:
        response = await async_client.get(f"/teacher/{login}")
    assert response.status_code == status.HTTP_200_OK


# UPDATE
@pytest.mark.asyncio
async def test_update_teacher():
    data = {        
        "cpf": "17553041025",
        "habilidades": "Test Address",
        "data_nascimento": "2000-01-01",
        "email": "test_amis@gmail.com",
        "login": "amisteste2",
        "nome": "amisteste1",
        "senha": "testpassword",
        "telefone": "12234567890"
    }
    async with AsyncClient(base_url=HTTPS_TEACHER, timeout=30.0) as async_client:
        response = await async_client.put("/teacher/amisteste2", json=data)
    assert response.status_code == status.HTTP_200_OK

# DELETE
@pytest.mark.asyncio
async def test_delete_teacher():
    async with AsyncClient(base_url=HTTPS_TEACHER, timeout=30.0) as async_client:
        response = await async_client.delete("/teacher/amisteste2")
    assert response.status_code == status.HTTP_204_NO_CONTENT