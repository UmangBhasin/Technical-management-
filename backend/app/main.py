from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api import api_router
from app.core.config import CORS_ORIGINS
from app.core.database import Base, SessionLocal, engine
from app.services.bootstrap_service import BootstrapService

app = FastAPI(title="Event Management System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_admin_user()


def seed_admin_user():
    db: Session = SessionLocal()
    try:
        BootstrapService.seed_admin_user(db)
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(api_router)
