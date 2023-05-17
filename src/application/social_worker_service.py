from ..domain.repositories.social_worker_repository import SocialWorkerRepositoryBaseModel
from ..domain.repositories.tokens_repository import TokensRepositoryBaseModel
from src.security import verify_password
from src.domain.models.social_worker import SocialWorker
from fastapi import HTTPException

class SocialWorkerService():
  __socialWorkersRepository__: SocialWorkerRepositoryBaseModel
  __tokensRepository__: TokensRepositoryBaseModel

  def __init__(
      self,
      socialWorkersRepository: SocialWorkerRepositoryBaseModel,
      tokensRepository: TokensRepositoryBaseModel
  ):
    self.__socialWorkersRepository__ = socialWorkersRepository
    self.__tokensRepository__ = tokensRepository

  def login(self, username: str , password: str ) -> tuple[str, str]:
    socialWorker = self.__socialWorkersRepository__.find_by_login(username)

    if not socialWorker or not verify_password(password, socialWorker.senha):
      raise HTTPException(
        status_code=403,
        detail="Email ou nome de usuário incorretos"
      )

    userToken = self.__tokensRepository__.createUserToken(socialWorker.login)
    refreshToken = self.__tokensRepository__.createRefreshToken(socialWorker.login)

    return (userToken, refreshToken)

  def verifyToken (self, token:str ) -> SocialWorker:
    userLogin = self.__tokensRepository__.verifyToken(token=token)
    socialWorker = self.__socialWorkersRepository__.find_by_login(userLogin)

    return socialWorker
  
  def refreshSession(self, refresh_token: str) -> tuple[str, str] | None:
    print("Token recebido: ", refresh_token)
    isRefreshTokenValid = self.__tokensRepository__.verifyToken(token=refresh_token)
    
    if isRefreshTokenValid:
      return self.__tokensRepository__.refreshToken(refresh_token=refresh_token)

    return None