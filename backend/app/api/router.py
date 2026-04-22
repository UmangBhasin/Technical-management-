from fastapi import APIRouter

from app.routers import auth, maintenance, membership, reports, transactions, users

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(membership.router, prefix="/memberships", tags=["Membership"])
api_router.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenance"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
