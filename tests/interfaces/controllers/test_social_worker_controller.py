import pytest
from httpx import AsyncClient
from fastapi import status



GLOBAL_RESPONSE = []
HTTPS_ASSISTENTE = "http://localhost:9090"

# CREATE
# @pytest.mark.asyncio
# async def test_create_assistente():
#     '''Função para testar a criação de uma assistente'''
#     data = {
#         "nome": "amisteste1",
#         "login": "amisteste1",
#         "senha": "123456789",
#         "cpf": "41575318091",
#         "dNascimento": "2001-01-28",
#         "observacao": "string",
#         "telefone": "61986051611",
#         "email": "testamis@gmail.com",
#         "administrador": True
#     }
#     async with AsyncClient(base_url=HTTPS_ASSISTENTE) as async_client:
#         response = await async_client.post("/socialWorker/", json=data)
#     assert response.status_code == status.HTTP_201_CREATED

# GET ALL
# @pytest.mark.asyncio
# async def test_read_all_assistente():
#     '''Função para testar exibição de todas socialWorker (ainda sem paginação)'''
#     async with AsyncClient(base_url=HTTPS_ASSISTENTE) as async_client:
#         response = await async_client.get("/socialWorker/")
#     assert response.status_code == status.HTTP_200_OK


# FIND BY LOGIN
# @pytest.mark.asyncio
# async def test_find_by_login_assistente():
#     '''Função para testar a busca de uma assistente por login'''
#     login = "amisteste1"
#     async with AsyncClient(base_url=HTTPS_ASSISTENTE) as async_client:
#         response = await async_client.get(f"/socialWorker/{login}")
#     assert response.status_code == status.HTTP_200_OK
#

# UPDATE
# @pytest.mark.asyncio
# async def test_update_assistente():
#     '''Função para testar a atualização de uma assistente'''
#     data = {
#         "nome": "amisteste1",
#         "login": "amisteste1",
#         "senha": "123456789",
#         "cpf": "41575318091",
#         "dNascimento": "2001-01-28",
#         "observacao": "string",
#         "telefone": "61986051611",
#         "email": "testamis2@gmail.com", #mudando email
#         "administrador": False
#     }
#     async with AsyncClient(base_url=HTTPS_ASSISTENTE) as async_client:
#         response = await async_client.put("/socialWorker/amisteste1", json=data)
#     assert response.status_code == status.HTTP_200_OK

# DELETE
# @pytest.mark.asyncio
# async def test_delete_assistente():
#     '''Função para testar a exclusão de uma assistente'''
#     async with AsyncClient(base_url=HTTPS_ASSISTENTE) as async_client:
#         response = await async_client.delete("/socialWorker/amisteste1")
#     assert response.status_code == status.HTTP_204_NO_CONTENT
