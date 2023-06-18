from fastapi import APIRouter, Form, Header, HTTPException
from infrastructure.repositories.social_worker_repository import SocialWorkerRepository
from infrastructure.repositories.tokens_repository import TokensRepository
from application.social_worker_service import SocialWorkerService
from infrastructure.repositories.tokens_repository import TokensRepository

from fastapi import APIRouter, Form, Header, HTTPException, status

from interfaces.controllers import socialWorkersService
from interfaces.controllers import studentService
from interfaces.controllers import teacherService
from interfaces.controllers import supervisorService

routerLoginSocialWorker = APIRouter(
    prefix="/login",
    tags=["login: social worker"],
    responses={404: {"description": "Not found"}},
)


@routerLoginSocialWorker.post("/socialWorker/")
async def login(username: str = Form(...), password: str = Form(...)):
    access_token, refresh_token = socialWorkersService.login(
        username=username, password=password
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@routerLoginSocialWorker.get("/socialWorker/token", status_code=201)
async def verificarToken(authorization: str = Header(...)):
    socialWorker = socialWorkersService.verifyToken(authorization)
    socialWorker.senha = None
    return socialWorker


@routerLoginSocialWorker.post("/socialWorker/token/refresh", status_code=201)
async def refreshToken(refresh_token: str = Header(...)):
    tokens = socialWorkersService.refreshSession(refresh_token=refresh_token)
    if tokens:
        return {
            "access_token": tokens[0],
            "refresh_token": tokens[1],
            "token_type": "bearer",
        }

    raise HTTPException(401, "Not Allowed")


@routerLoginSocialWorker.post("/socialWorker/logout")
def logout(refresh_token: str = Header(...)):
    socialWorkersService.delete_refresh_token(refresh_token)

    return {"message": "Logout realizado com sucesso"}


routerLoginStudent = APIRouter(
    prefix="/login",
    tags=["login: student"],
    responses={404: {"description": "Not found"}},
)


@routerLoginStudent.post("/student/")
async def login(username: str = Form(...), password: str = Form(...)):
    access_token, refresh_token = studentService.login(
        username=username, password=password
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@routerLoginStudent.get("/student/token", status_code=201)
async def verificarToken(authorization: str = Header(...)):
    student = studentService.verifyToken(authorization)
    student.senha = None
    return student


@routerLoginStudent.post("/student/token/refresh", status_code=201)
async def refreshToken(refresh_token: str = Header(...)):
    tokens = studentService.refreshSession(refresh_token=refresh_token)
    if tokens:
        return {
            "access_token": tokens[0],
            "refresh_token": tokens[1],
            "token_type": "bearer",
        }

    raise HTTPException(401, "Not Allowed")


@routerLoginStudent.post("/student/logout")
def logout(refresh_token: str = Header(...)):
    studentService.delete_refresh_token(refresh_token)

    return {"message": "Logout realizado com sucesso"}


routerLoginTeacher = APIRouter(
    prefix="/login",
    tags=["login: teacher"],
    responses={404: {"description": "Not found"}},
)


@routerLoginTeacher.post("/teacher/")
async def login(username: str = Form(...), password: str = Form(...)):
    access_token, refresh_token = teacherService.login(
        username=username, password=password
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@routerLoginTeacher.get("/teacher/token", status_code=201)
async def verificarToken(authorization: str = Header(...)):
    teacher = teacherService.verifyToken(authorization)
    teacher.senha = None
    return teacher


@routerLoginTeacher.post("/teacher/token/refresh", status_code=201)
async def refreshToken(refresh_token: str = Header(...)):
    tokens = teacherService.refreshSession(refresh_token=refresh_token)
    if tokens:
        return {
            "access_token": tokens[0],
            "refresh_token": tokens[1],
            "token_type": "bearer",
        }

    raise HTTPException(401, "Not Allowed")


@routerLoginTeacher.post("/teacher/logout")
def logout(refresh_token: str = Header(...)):
    teacherService.delete_refresh_token(refresh_token)

    return {"message": "Logout realizado com sucesso"}

routerLoginSupervisor = APIRouter(
    prefix="/login",
    tags=["login: supervisor"],
    responses={404: {"description": "Not found"}},
)

@routerLoginSupervisor.post("/supervisor/")
async def login(username: str = Form(...), password: str = Form(...)):
    access_token, refresh_token = supervisorService.login(
        username=username, password=password
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@routerLoginSupervisor.get("/supervisor/token", status_code=201)
async def verificarToken(authorization: str = Header(...)):
    supervisor = supervisorService.verifyToken(authorization)
    supervisor.senha = None
    return supervisor

@routerLoginSupervisor.post("/supervisor/token/refresh", status_code=201)
async def refreshToken(refresh_token: str = Header(...)):
    tokens = supervisorService.refreshSession(refresh_token=refresh_token)
    if tokens:
        return {
            "access_token": tokens[0],
            "refresh_token": tokens[1],
            "token_type": "bearer",
        }

    raise HTTPException(401, "Not Allowed")

@routerLoginSupervisor.post("/supervisor/logout")
def logout(refresh_token: str = Header(...)):
    supervisorService.delete_refresh_token(refresh_token)

    return {"message": "Logout realizado com sucesso"}

