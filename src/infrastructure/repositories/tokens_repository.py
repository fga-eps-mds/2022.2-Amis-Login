from datetime import datetime, timedelta
from jose import jwt
from typing import Union, Any
from src.domain.models.tokens import RefreshTokens
from src.domain.repositories.tokens_repository import TokensRepositoryBaseModel
from src.security import ACCESS_TOKEN_EXPIRE_HOURS, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_HOURS

class TokensRepository():
  __RefreshTokens__: list[RefreshTokens] = []

  def createUserToken(self, subject: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        hours=ACCESS_TOKEN_EXPIRE_HOURS
    )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

  def createRefreshToken(self, login: str) -> str:
      expire = datetime.utcnow() + timedelta(
          hours=REFRESH_TOKEN_EXPIRE_HOURS
      )
      to_encode = {"exp": expire, "sub": login}
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

      for token in self.__RefreshTokens__:
        if token.login == login:
          token.refreshToken = encoded_jwt
          break

      id = len(self.__RefreshTokens__)
      self.__RefreshTokens__.append(RefreshTokens(id=id, login=login, refreshToken=encoded_jwt))
      return encoded_jwt

  '''Returns userToken and refreshToken'''
  def refreshToken(self, refresh_token: str) -> tuple[str, str] | None:
    refresh_token = refresh_token.split(" ")[1]
    for index, token in enumerate(self.__RefreshTokens__):
      if(token.refreshToken == refresh_token):
        self.__RefreshTokens__[index].refreshToken = self.createRefreshToken(token.login)

        newRefreshToken = token.refreshToken
        newUserToken = self.createUserToken(token.login)
        return (newUserToken, newRefreshToken)

    return None
  
  def verifyToken(self, token: str) -> Any:
    decodedJwt = jwt.decode(token.split(" ")[1], SECRET_KEY, ALGORITHM).get('sub')
    
    return decodedJwt

