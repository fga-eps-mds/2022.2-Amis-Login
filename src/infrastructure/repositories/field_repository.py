from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re


@dataclass
class fieldInfo:
    """Classe para armazenar informações sobre os campos de um modelo"""
    status: bool
    detail: str


class FieldValidation:
    """Validação quanto ao formato dos dados (não valida lógicas de negócio))"""
    @classmethod
    def nomeValidation(cls, nome: str) -> fieldInfo:
        if len(nome) > 70:
            return fieldInfo(False, "Nome muito grande")
        elif len(nome) == 0:
            return fieldInfo(False, "Nome não pode ser vazio")
        return fieldInfo(True, "Nome válido")

    @classmethod
    def dNascimentoValidation(cls, dNascimento: str) -> fieldInfo:
        if len(dNascimento) > 10:
            return fieldInfo(False, "Data de nascimento muito grande")
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, dNascimento):
            return fieldInfo(False, "Formato data de nascimento inválida")

        try:
            datetime.strptime(dNascimento, '%Y-%m-%d')
        except Exception as e:
            return fieldInfo(False, f"Data de nascimento inválida ({e})")

        return fieldInfo(True, "Data de nascimento válida")

    @classmethod
    def cpfValidation(cls, cpf: str) -> fieldInfo:
        if len(cpf) > 11:
            return fieldInfo(False, "CPF muito grande")

        pattern = r'^\d{11}$'
        if not re.match(pattern, cpf):
            return fieldInfo(False, "Formato CPF inválido")

        if cpf == cpf[0]*11:
            return fieldInfo(False, "CPF inválido")

        sum0 = sum([int(cpf[i])*(10-i) for i in range(9)])
        rest = (sum0*10) % 11
        if rest != 10 and rest != int(cpf[9]):
            return fieldInfo(False, "CPF inválido")

        sum0 = sum([int(cpf[i])*(11-i) for i in range(10)])
        rest = (sum0*10) % 11
        if rest != 10 and rest != int(cpf[10]):
            return fieldInfo(False, "CPF inválido")

        return fieldInfo(True, "CPF válido")

    @classmethod
    def telefoneValidation(cls, telefone: str) -> fieldInfo:
        if len(telefone) > 11:
            return fieldInfo(False, "Telefone muito grande")

        pattern = r'^\d{11}$'
        if not re.match(pattern, telefone):
            return fieldInfo(False, "Telefone inválido")

        return fieldInfo(True, "Telefone válido")

    @classmethod
    def emailValidation(cls, email: str) -> fieldInfo:
        if len(email) > 100:
            return fieldInfo(False, "Email muito grande")

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return fieldInfo(False, "Email inválido")

        return fieldInfo(True, "Email válido")

    @classmethod
    def senhaValidation(cls, senha: str) -> fieldInfo:
        if len(senha) < 8:
            return fieldInfo(False, "Senha muito pequena")

        return fieldInfo(True, "Senha válida")

    @classmethod
    def observacaoValidation(cls, observacao: str) -> fieldInfo:
        if len(observacao) > 200:
            return fieldInfo(False, "Observação muito grande")

        return fieldInfo(True, "Observação válida")

    @classmethod
    def loginValidation(cls, login: str) -> fieldInfo:
        if len(login) < 8:
            return fieldInfo(False, "Login muito pequeno")

        return fieldInfo(True, "Login válido")
    
    @classmethod
    def statusValidation(cls, status: Enum):
        if status.value < 1 or status.value > 3:
            return fieldInfo(False, "Status inválido")
        
        return fieldInfo(True, "Status válido")
    
    @classmethod
    def cepValidation(cls, cep : str):
        if len(cep) > 8:
            return fieldInfo(False, "CEP muito grande")
        
        pattern = r'^\d{8}$'
        if not re.match(pattern, cep):
            return fieldInfo(False, "Formato de CEP inválido")
        
        return fieldInfo(True, "CEP válido")
    
    @classmethod
    def bairroValidation(cls, bairro : str):
        if len(bairro) > 100:
            return fieldInfo(False, "Bairro muito grande")
        
        return fieldInfo(True, "Bairro válido")
    
    @classmethod
    def cidadeValidation(cls, cidade : str):
        if len(cidade) > 100:
            return fieldInfo(False, "Cidade muito grande")
        
        return fieldInfo(True, "Cidade válida")
    
    @classmethod
    def descricaoValidation(cls, descricao:str):
        if len(descricao > 100):
            return fieldInfo(False,"Descrição muito grande")
        return fieldInfo(True,"Descrição válida")
        
