from pydantic import BaseModel

class RefreshTokens(BaseModel):
  id: int
  login: str
  refreshToken: str
