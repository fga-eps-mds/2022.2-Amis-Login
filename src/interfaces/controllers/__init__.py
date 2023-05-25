from src.application.social_worker_service import SocialWorkerService
from src.infrastructure.repositories.tokens_repository import TokensRepository
from src.infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from src.database import get_db

[databaseSession] = get_db()
socialWorkerRepository = SocialWorkerRepository(databaseSession)
tokensRepository = TokensRepository()
socialWorkersService = SocialWorkerService(
  socialWorkersRepository=socialWorkerRepository,
  tokensRepository=tokensRepository
)