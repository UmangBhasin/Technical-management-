from sqlalchemy import func
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_db, require_admin
from app.models.maintenance import Maintenance
from app.models.membership import Membership
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.report import DashboardReport, MonthlyRevenuePoint

router = APIRouter()


@router.get("/dashboard", response_model=DashboardReport)
def dashboard_report(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":
        total_users = db.query(func.count(User.id)).scalar() or 0
        total_memberships = db.query(func.count(Membership.id)).scalar() or 0
        active_memberships = db.query(func.count(Membership.id)).filter(Membership.status == "active").scalar() or 0
        total_transactions = db.query(func.count(Transaction.id)).scalar() or 0
        total_revenue = db.query(func.coalesce(func.sum(Transaction.amount), 0.0)).scalar() or 0.0
        total_maintenance_cost = db.query(func.coalesce(func.sum(Maintenance.cost), 0.0)).scalar() or 0.0
    else:
        total_users = 1
        total_memberships = db.query(func.count(Membership.id)).scalar() or 0
        active_memberships = db.query(func.count(Membership.id)).filter(Membership.status == "active").scalar() or 0
        total_transactions = (
            db.query(func.count(Transaction.id)).filter(Transaction.created_by == current_user.id).scalar() or 0
        )
        total_revenue = (
            db.query(func.coalesce(func.sum(Transaction.amount), 0.0))
            .filter(Transaction.created_by == current_user.id)
            .scalar()
            or 0.0
        )
        total_maintenance_cost = 0.0

    return DashboardReport(
        total_users=total_users,
        total_memberships=total_memberships,
        active_memberships=active_memberships,
        total_transactions=total_transactions,
        total_revenue=float(total_revenue),
        total_maintenance_cost=float(total_maintenance_cost),
    )


@router.get("/monthly-revenue", response_model=list[MonthlyRevenuePoint])
def monthly_revenue(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.strftime("%Y-%m", Transaction.transaction_date).label("month"),
            func.coalesce(func.sum(Transaction.amount), 0.0).label("revenue"),
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    return [MonthlyRevenuePoint(month=row.month, revenue=float(row.revenue)) for row in rows]
