from  domain.repositories.student_repository import StudentRepository 
from  domain.models.student import StudentBase 
from src.domain.repositories.tokens_repository import TokensRepositoryBaseModel
from src.security import verify_password
from  fastapi import HTTPException


class StudentService():
    __studentService__ : StudentRepository
    __tokensRepository__: TokensRepositoryBaseModel
    
    def __init__(
          self, studentRepository: StudentRepository,
          tokensRepository: TokensRepositoryBaseModel
  ):
       self.__studentRepository__ = studentRepository
       self.__tokensRepository__ = tokensRepository

    def login(self, username: str , password: str ) -> tuple[str, str]:
       student = self.__studentRepository__.find_by_login_student(username)
       if not student or not verify_password(password, student.senha):
          raise HTTPException(
             status_code=401,
             detail="Email ou nome de usuário incorretos"
             )
       
       userToken = self.__tokensRepository__.createUserToken(student.login)
       refreshToken = self.__tokensRepository__.createRefreshToken(student.login)
       
       return(userToken, refreshToken)
       
    def verifyToken(self,token:str) -> StudentBase:
       userLogin = self.__tokensRepository__.verifyToken(token=token)
       student = self.__studentRepository__.find_by_login_student(userLogin)
       
       return student
    
    def refreshSession(self, refresh_token: str) -> tuple[str, str] | None:
       print("Token recebido: ", refresh_token)
       isRefreshTokenValid = self.__tokensRepository__.verifyToken(token= refresh_token)
       
       if isRefreshTokenValid:
          return self.__tokensRepository__.refreshToken(refresh_token = refresh_token)
       return None

       
    

 