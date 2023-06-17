from sqlalchemy.orm import Session
from ..models.supervisor import Supervisor
from typing import List, runtime_checkable, Protocol


@runtime_checkable
class SupervisorRepository(Protocol):
    
    def save_supervisor(self, supervisor: Supervisor) -> Supervisor:
        ...

    def find_all_supervisor(self) -> List[Supervisor]:
        ...

    def find_by_login_supervisor(self, login : str) -> Supervisor:
        ...

    def exists_by_cpf_supervisor(self, cpf: str) -> bool:
        ...

    def delete_by_login_supervisor(self, login: str) -> None:
        ...

    def update_by_login(self, supervisor_request: Supervisor) -> Supervisor:
        ...

    def validate_supervisor(self, supervisor: Supervisor) -> dict:
        ...
