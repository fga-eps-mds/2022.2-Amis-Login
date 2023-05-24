from application.social_worker_service import SocialWorkerService
from infrastructure.repositories.tokens_repository import TokensRepository
from infrastructure.repositories.social_worker_repository import SocialWorkerRepository


socialWorkerRepository = SocialWorkerRepository()
tokensRepository = TokensRepository()
socialWorkersService = SocialWorkerService(
  socialWorkersRepository=socialWorkerRepository,
  tokensRepository=tokensRepository
)