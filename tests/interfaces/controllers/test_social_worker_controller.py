import pytest
from httpx import AsyncClient
from fastapi import status



GLOBAL_RESPONSE = []
HTTPS_ASSISTENTE = "http://localhost:9090"

# CREATE
@pytest.mark.asyncio
async def test_create_assistente():
    '''Função para testar a criação de uma assistente'''
    data = {
        "nome": "amisteste1",
        "login": "amisteste1",
        "senha": "123456789",
        "cpf": "41575318091",
        "dNascimento": "2001-01-28",
        "observacao": "string",
        "telefone": "61986051611",
        "email": "testamis@gmail.com",
        "administrador": True
    }
    async with AsyncClient(base_url=HTTPS_ASSISTENTE) as async_client:
        response = await async_client.post("/socialWorker/", json=data)
    assert response.status_code == status.HTTP_201_CREATED

# GET ALL
@pytest.mark.asyncio
async def test_read_all_assistente():
    '''Função para testar exibição de todas socialWorker (ainda sem paginação)'''
    async with AsyncClient(base_url=HTTPS_ASSISTENTE) as async_client:
        response = await async_client.get("/socialWorker/")
    assert response.status_code == status.HTTP_200_OK



