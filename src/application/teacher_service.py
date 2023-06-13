from domain.models.teacher import Teacher, TeacherDB, TeacherRequest
from domain.repositories.tokens_repository import TokensRepositoryBaseModel
from security import verify_password
from domain.repositories.teacher_repository import TeacherRepositoryBaseModel
from fastapi import HTTPException, status
from infrastructure.repositories.field_repository import FieldValidation


class TeacherService:
    __teachersRepository__: TeacherRepositoryBaseModel
    __tokensRepository__: TokensRepositoryBaseModel

    def __init__(
        self,
        teachersRepository: TeacherRepositoryBaseModel,
        tokensRepository: TokensRepositoryBaseModel,
    ):
        self.__teachersRepository__ = teachersRepository
        self.__tokensRepository__ = tokensRepository

    def login(self, username: str, password: str) -> tuple[str, str]:
        teacher = self.__teachersRepository__.find_by_login(username)

        if not teacher or not verify_password(password, teacher.senha):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email ou nome de usuário incorretos",
            )

        userToken = self.__tokensRepository__.createUserToken(teacher.login)
        refreshToken = self.__tokensRepository__.createRefreshToken(teacher.login)

        return (userToken, refreshToken)

    def verifyToken(self, token: str) -> Teacher:
        userLogin = self.__tokensRepository__.verifyToken(token=token)
        teacher = self.__teachersRepository__.find_by_login(userLogin)
        ### Vai quebrar

        return teacher

    def refreshSession(self, refresh_token: str) -> tuple[str, str] | None:
        print("Token recebido: ", refresh_token)
        isRefreshTokenValid = self.__tokensRepository__.verifyToken(token=refresh_token)

        if isRefreshTokenValid:
            return self.__tokensRepository__.refreshToken(refresh_token=refresh_token)

        return None

    def find_by_login(self, login: str) -> Teacher | None:
        """Dado o login do professor, retorna o objeto da professor, ou None se não existir"""
        return self.__teachersRepository__.find_by_login(login=login)

    def find_all(self) -> list[TeacherDB]:
        """Faz uma query de todos os objetos professor na DB,
        e retorna somente com os atributos Teacher"""
        # father_attributes = {key: value for key, value in vars(child_obj).items() if key in vars(Father).keys()}
        teachers_db = self.__teachersRepository__.find_all()
        teachers = list()
        for teacher_db in teachers_db:
            teacher = Teacher(
                login=teacher_db.login,
                cpf=teacher_db.cpf,
                habilidades=teacher_db.habilidades,
                data_nascimento=teacher_db.data_nascimento,
                email=teacher_db.email,
                nome=teacher_db.nome,
                senha=teacher_db.senha,
                telefone=teacher_db.telefone,
            )
            teachers.append(teacher)
        return teachers

    def validate_teacher(self, teacher: TeacherRequest) -> dict:
        """Função para validar os campos de um objeto Teacher"""

        fieldInfoDict = {}
        fieldInfoDict["nome"] = vars(FieldValidation.nomeValidation(teacher.nome))
        fieldInfoDict["cpf"] = vars(FieldValidation.cpfValidation(teacher.cpf))
        fieldInfoDict["dNascimento"] = vars(
            FieldValidation.dNascimentoValidation(teacher.data_nascimento)
        )
        fieldInfoDict["telefone"] = vars(
            FieldValidation.telefoneValidation(teacher.telefone)
        )
        fieldInfoDict["email"] = vars(FieldValidation.emailValidation(teacher.email))
        fieldInfoDict["senha"] = vars(FieldValidation.senhaValidation(teacher.senha))

        completeStatus = True
        for key in fieldInfoDict:
            if fieldInfoDict[key]["status"] == False:
                completeStatus = False
                break
        fieldInfoDict["completeStatus"] = completeStatus

        return fieldInfoDict

    def exists_by_login(self, login: str) -> bool:
        """Função para verificar se existe um objeto Teacher com o login dado"""
        return self.__teachersRepository__.find_by_login(login=login) is not None

    def delete_refresh_token(self, refresh_token: str):
        self.__tokensRepository__.delete_refresh_token(refresh_token)
        return None

    def save(self, teacherSent: TeacherDB) -> TeacherDB:
        """Função para salvar um objeto Teacher na DB, utilizada também como update"""
        return self.__teachersRepository__.save(teacherSent=teacherSent)

    def delete_by_login(self, login: str) -> None:
        """Função para excluir um objeto Teacher da DB dado o login"""
        self.__teachersRepository__.delete_by_login(login=login)
