from pydantic import BaseModel

##### Aluno ####
class AlunoBase(BaseModel):
    bairro : str
    cep : str
    cidade : str
    cpf : str
    data_nascimento : str 
    deficiencia : bool 
    descricao_endereco : str 
    email : str 
    nome : str 
    nome_social : str 
    rg : str
    senha : str

class AlunoRequest(AlunoBase):
    ...

class AlunoResponse(AlunoBase):
    cpf : int

    class Config:
        orm_mode = True

#### Telefone #####

class TelefoneBase(BaseModel):
    ddd : int
    numero : str
    tipo_numero : str
    cpf_aluno: str

class TelefoneRequest(TelefoneBase):
    ...

class TelefoneResponse(TelefoneBase):
    id_telefone : int
    cpf_aluno: str
    
    class Config:
        orm_mode = True


    

