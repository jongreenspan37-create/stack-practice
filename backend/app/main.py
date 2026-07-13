from fastapi import FastAPI
from sqlalchemy import text
from .database import engine
from app.users.routers import router as users_router

app = FastAPI()

app.include_router(users_router)

@app.get("/")
def homepage():
    return {"message": "This is public — anyone can see it"}

