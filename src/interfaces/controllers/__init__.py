from src.database import get_db
from src.application.social_worker_service import SocialWorkerService
from src.infrastructure.repositories.tokens_repository import TokensRepository
from src.infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from src.application.student_service import StudentService
from src.infrastructure.repositories.student_repository import StudentRepository
from src.database import SessionLocal

databaseSessionGenerator = SessionLocal
studentRepository = StudentRepository(databaseSessionGenerator)
tokensRepository = TokensRepository()
studentService = StudentService(
    studentRepository = studentRepository,
    tokensRepository=tokensRepository
)


socialWorkerRepository = SocialWorkerRepository(databaseSessionGenerator)
socialWorkersService = SocialWorkerService(
  socialWorkersRepository=socialWorkerRepository,
  tokensRepository=tokensRepository
)
