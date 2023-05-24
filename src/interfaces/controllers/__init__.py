from src.application.student_service import StudentService
from src.infrastructure.repositories.tokens_repository import TokensRepository
from src.infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from src.infrastructure.repositories.student_repository import StudentRepository
from src.database import get_db

[databaseSession] = get_db()
studentRepository = StudentRepository(databaseSession)
tokensRepository = TokensRepository()
studentService = StudentService(
    studentRepository = studentRepository,
    tokensRepository=tokensRepository
)

