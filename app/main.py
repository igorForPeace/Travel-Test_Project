from fastapi import FastAPI
from app.db import Base, engine
from app import models
from app.routers.projects import router


app = FastAPI(title="Travel Project")
Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/projects", tags=["projects"])


@app.get("/health")
def health():
    return {"status": "ok"}