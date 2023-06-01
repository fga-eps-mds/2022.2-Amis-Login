from domain.repositories.student_repository import StudentRepository
from domain.models.student import Student, StudentBase, StudentRequest
from domain.repositories.tokens_repository import TokensRepositoryBaseModel
from infrastructure.repositories.field_repository import FieldValidation

from security import verify_password
from fastapi import HTTPException


class StudentService():
    __studentService__: StudentRepository
    __tokensRepository__: TokensRepositoryBaseModel

    def __init__(
        self, studentRepository: StudentRepository,
        tokensRepository: TokensRepositoryBaseModel
    ):
        self.__studentRepository__ = studentRepository
        self.__tokensRepository__ = tokensRepository

    def login(self, username: str, password: str) -> tuple[str, str]:
        student = self.__studentRepository__.find_by_login_student(username)
        if not student or not verify_password(password, student.senha):
            raise HTTPException(
                status_code=401,
                detail="Email ou nome de usuário incorretos"
            )

        userToken = self.__tokensRepository__.createUserToken(student.login)
        refreshToken = self.__tokensRepository__.createRefreshToken(
            student.login)

        return (userToken, refreshToken)

    def verifyToken(self, token: str) -> StudentBase:
        userLogin = self.__tokensRepository__.verifyToken(token=token)
        student = self.__studentRepository__.find_by_login_student(userLogin)

        return student

    def refreshSession(self, refresh_token: str) -> tuple[str, str] | None:
        print("Token recebido: ", refresh_token)
        isRefreshTokenValid = self.__tokensRepository__.verifyToken(
            token=refresh_token)

        if isRefreshTokenValid:
            return self.__tokensRepository__.refreshToken(refresh_token=refresh_token)
        return None

    def find_by_login(self, login: str) -> Student | None:
        return self.__studentRepository__.find_by_login_student(login)
    
    def find_all(self) -> list[Student]:
        students_db = self.__studentRepository__.find_all_student()
        students = list()

        for student_db in students_db:
            student = Student(
                bairro = student_db.bairro,
                cep = student_db.cep,
                cidade = student_db.cidade,
                cpf = student_db.cpf,
                data_nascimento= student_db.data_nascimento,
                deficiencia = student_db.deficiencia,
                descricao_endereco = student_db.descricao_endereco,
                email= student_db.email,
                login= student_db.login,
                nome=student_db.nome,
                senha=student_db.senha,
                status= student_db.status,
                telefone= student_db.telefone
            )
            students.append(student)
        return students
    
    def exists_by_login(self, login: str) -> bool:
        '''Função para verificar se existe um objeto SocialWorker com o login dado'''
        return self.__studentRepository__.find_by_login_student(login) is not None

    def delete_refresh_token(self, refresh_token: str):
        self.__tokensRepository__.delete_refresh_token(refresh_token)
        return None

    def save(self, student: Student) -> Student:
        '''Função para salvar um objeto SocialWorker na DB, utilizada também como update'''
        return self.__studentRepository__.save_student(student)

    def delete_by_login(self, login: str) -> None:
        '''Função para excluir um objeto SocialWorker da DB dado o login'''
        self.__studentRepository__.delete_by_login_student(login)

    
    def validate_student(self, student: Student) -> dict:
        '''Função para validar os campos de um objeto SocialWorker'''

        fieldInfoDict = {}
        fieldInfoDict["bairro"] = vars(FieldValidation.bairroValidation(
            student.bairro))
        fieldInfoDict["cep"] = vars(FieldValidation.cepValidation(student.cep))
        fieldInfoDict["cidade"] = vars(FieldValidation.cidadeValidation(
            student.cidade))
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(student.cpf))
        fieldInfoDict["dNascimento"] = vars(FieldValidation.dNascimentoValidation(
        student.data_nascimento))
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(
            student.email))
        fieldInfoDict["login"] = vars(FieldValidation.loginValidation(
            student.login))
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(
            student.nome))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(
            student.senha))
        fieldInfoDict["status"] = vars(FieldValidation.statusValidation(
            student.status))
        fieldInfoDict["telefone"] = vars(FieldValidation.telefoneValidation(
            student.telefone))
        
        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]['status'] == False:
                completeStatus = False
                break
        fieldInfoDict['completeStatus'] = completeStatus

        return fieldInfoDict
        