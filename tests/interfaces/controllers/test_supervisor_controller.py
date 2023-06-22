import pytest
from httpx import AsyncClient
from fastapi import status

GLOBAL_RESPONSE = []
HTTPS_SUPERVISOR = "http://localhost:9090"

# CREATE
@pytest.mark.asyncio
async def test_create_supervisor():
    data = {        
        "cpf": "17553041025",
        "data_nascimento": "2000-01-01",
        "email"  : "testamis@gmail.com",
        "login": "amisteste2",
        "nome": "amisteste1",
        "senha": "testpassword",
        "telefone": "12234567890"
    }
    async with AsyncClient(base_url=HTTPS_SUPERVISOR, timeout=30.0) as async_client:
        response = await async_client.post("/supervisor/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

# GET ALL
@pytest.mark.asyncio
async def test_read_all_supervisor():
    async with AsyncClient(base_url=HTTPS_SUPERVISOR, timeout=30.0) as async_client:
        response = await async_client.get("/supervisor/")
    assert response.status_code == status.HTTP_200_OK

# FIND BY LOGIN
@pytest.mark.asyncio
async def test_find_by_login_supervisor():
    login = "amisteste2"
    async with AsyncClient(base_url=HTTPS_SUPERVISOR, timeout=30.0) as async_client:
        response = await async_client.get(f"/supervisor/{login}")
    assert response.status_code == status.HTTP_200_OK

#update
@pytest.mark.asyncio
async def test_update_supervisor():
    data = {        
        "cpf": "17553041025",
        "data_nascimento": "2000-01-01",
        "email"  : "testamis@gmail.com",
        "login": "amisteste2",
        "nome": "amisteste1",
        "senha": "testpassword",
        "telefone": "12234567890"
    }
    async with AsyncClient(base_url=HTTPS_SUPERVISOR, timeout=30.0) as async_client:
        response = await async_client.put("/supervisor/amisteste2", json=data)
    assert response.status_code == status.HTTP_200_OK

# DELETE
@pytest.mark.asyncio
async def test_delete_supervisor():
    async with AsyncClient(base_url=HTTPS_SUPERVISOR, timeout=30.0) as async_client:
        response = await async_client.delete("/supervisor/amisteste2")
    assert response.status_code == response.status_code == status.HTTP_204_NO_CONTENT