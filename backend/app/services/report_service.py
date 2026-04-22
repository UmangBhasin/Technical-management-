from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance
from app.models.membership import Membership
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.report import (
    DashboardReport,
    MembershipReportRow,
    MonthlyRevenuePoint,
    TransactionReportRow,
    UserReportRow,
)


class ReportService:
    @staticmethod
    def dashboard(db: Session, current_user: User) -> DashboardReport:
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

    @staticmethod
    def monthly_revenue(db: Session, current_user: User) -> list[MonthlyRevenuePoint]:
        query = db.query(
            func.strftime("%Y-%m", Transaction.transaction_date).label("month"),
            func.coalesce(func.sum(Transaction.amount), 0.0).label("revenue"),
        )

        if current_user.role != "admin":
            query = query.filter(Transaction.created_by == current_user.id)

        rows = query.group_by("month").order_by("month").all()
        return [MonthlyRevenuePoint(month=row.month, revenue=float(row.revenue)) for row in rows]

    @staticmethod
    def user_report(db: Session, current_user: User) -> list[UserReportRow]:
        query = db.query(
            User.id,
            User.full_name,
            User.email,
            User.role,
            User.is_active,
            User.created_at,
        )
        if current_user.role != "admin":
            query = query.filter(User.id == current_user.id)

        rows = query.order_by(User.created_at.desc()).all()
        return [
            UserReportRow(
                id=row.id,
                full_name=row.full_name,
                email=row.email,
                role=row.role,
                is_active=row.is_active,
                created_at=row.created_at,
            )
            for row in rows
        ]

    @staticmethod
    def membership_report(db: Session, current_user: User) -> list[MembershipReportRow]:
        query = db.query(
            Membership.id,
            Membership.member_name,
            Membership.email,
            Membership.membership_type,
            Membership.start_date,
            Membership.end_date,
            Membership.status,
        )
        if current_user.role != "admin":
            query = query.filter(Membership.created_by == current_user.id)

        rows = query.order_by(Membership.created_at.desc()).all()
        return [
            MembershipReportRow(
                id=row.id,
                member_name=row.member_name,
                email=row.email,
                membership_type=row.membership_type,
                start_date=row.start_date,
                end_date=row.end_date,
                status=row.status,
            )
            for row in rows
        ]

    @staticmethod
    def transaction_report(db: Session, current_user: User) -> list[TransactionReportRow]:
        query = (
            db.query(
                Transaction.id,
                Transaction.created_by.label("user_id"),
                User.full_name.label("user_name"),
                Membership.member_name.label("member_name"),
                Transaction.amount,
                Transaction.transaction_type,
                Transaction.transaction_date,
            )
            .join(User, User.id == Transaction.created_by)
            .join(Membership, Membership.id == Transaction.member_id)
        )

        if current_user.role != "admin":
            query = query.filter(Transaction.created_by == current_user.id)

        rows = query.order_by(Transaction.transaction_date.desc()).all()
        return [
            TransactionReportRow(
                id=row.id,
                user_id=row.user_id,
                user_name=row.user_name,
                member_name=row.member_name,
                amount=float(row.amount),
                transaction_type=row.transaction_type,
                transaction_date=row.transaction_date,
            )
            for row in rows
        ]
