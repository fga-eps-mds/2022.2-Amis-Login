from typing import Union, Any
from typing import Protocol, runtime_checkable


@runtime_checkable
class TokensRepositoryBaseModel(Protocol):
    def createUserToken(self, subject: Union[str, Any]) -> str:
        ...

    def createRefreshToken(self, userId: str) -> str:
        ...

    '''Returns userToken and refreshToken'''

    def refreshToken(self, refresh_token: str) -> tuple[str, str] | None:
        ...

    '''Returns login'''

    def verifyToken(self, token: str) -> Any:
        ...
