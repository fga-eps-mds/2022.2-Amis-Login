from interfaces.controllers.social_worker_controller import router as assistente_router
from interfaces.controllers.user_controller import router as login_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv

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


app.include_router(login_router)
app.include_router(assistente_router)


@app.get('/')
async def root():
    return {"message": "Amis !"}
