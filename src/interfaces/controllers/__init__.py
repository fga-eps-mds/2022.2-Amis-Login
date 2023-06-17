from database import get_db
from application.social_worker_service import SocialWorkerService
from application.teacher_service import TeacherService
from application.student_service import StudentService
from application.supervisor_service import SupervisorService
from infrastructure.repositories.tokens_repository import TokensRepository
from infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from infrastructure.repositories.teacher_repository import TeacherRepository
from infrastructure.repositories.student_repository import StudentRepository
from infrastructure.repositories.supervisor_repository import SupervisorRepository

from database import SessionLocal

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

teacherRepository = TeacherRepository(databaseSessionGenerator)
teacherService = TeacherService(
  teachersRepository=teacherRepository,
  tokensRepository=tokensRepository
)

supervisorRepository = SupervisorRepository(databaseSessionGenerator)
tokensRepository = TokensRepository()
supervisorService = SupervisorService(
    supervisorRepository = supervisorRepository,
    tokensRepository=tokensRepository
)
