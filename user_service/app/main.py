from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.v1.routes import users


Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

app.include_router(users.router)