from dotenv import load_dotenv
load_dotenv()
from interfaces.controllers.user_controller import router as login_router
from interfaces.controllers.social_worker_controller import router as assistente_router
from interfaces.controllers.student_controller import router_student
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
app.include_router(login_router)
app.include_router(router_student)
app.include_router(assistente_router)


@app.get('/')
async def root():
    return {"message": "Amis !"}
