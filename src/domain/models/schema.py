from typing import Union
from pydantic import BaseModel
from domain.models.social_worker import SocialWorker


class SocialWorkerRequest(SocialWorker):
    '''...'''
    pass


class SocialWorkerResponse(SocialWorker):
    '''...'''
    class Config:
        orm_mode = True
