from dotenv import load_dotenv

load_dotenv()
from interfaces.controllers.user_controller import (
    routerLoginSocialWorker,
    routerLoginStudent,
    routerLoginTeacher,
    routerLoginSupervisor
)
from interfaces.controllers.social_worker_controller import router as router_assistente
from interfaces.controllers.student_controller import router_student
from interfaces.controllers.teacher_controller import router_teacher
from interfaces.controllers.supervisor_controller import router_supervisor
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

load_dotenv()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(routerLoginSocialWorker)
app.include_router(routerLoginTeacher)
app.include_router(routerLoginStudent)
app.include_router(routerLoginSupervisor)
app.include_router(router_student)
app.include_router(router_assistente)
app.include_router(router_teacher)
app.include_router(router_supervisor)

@app.get("/")
async def root():
    return {"message": "Amis !"}