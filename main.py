from fastapi import FastAPI
from app.routers import client_user, ops_user
from app.routers import file
app = FastAPI(title="Secure File Sharing System")

app.include_router(client_user.router)
app.include_router(ops_user.router)
app.include_router(file.router)
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)
