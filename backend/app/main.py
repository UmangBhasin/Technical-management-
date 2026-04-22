from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import ADMIN_DEFAULT_EMAIL, ADMIN_DEFAULT_NAME, ADMIN_DEFAULT_PASSWORD, CORS_ORIGINS
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.user import User
from app.routers import auth, maintenance, membership, reports, transactions, users

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
        existing_admin = db.query(User).filter(User.email == ADMIN_DEFAULT_EMAIL).first()
        if not existing_admin:
            admin_user = User(
                full_name=ADMIN_DEFAULT_NAME,
                email=ADMIN_DEFAULT_EMAIL,
                password_hash=hash_password(ADMIN_DEFAULT_PASSWORD),
                role="admin",
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(membership.router, prefix="/api/memberships", tags=["Membership"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["Maintenance"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
