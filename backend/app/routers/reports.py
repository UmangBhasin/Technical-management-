from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.report import (
    DashboardReport,
    MembershipReportRow,
    MonthlyRevenuePoint,
    TransactionReportRow,
    UserReportRow,
)
from app.services.report_service import ReportService

router = APIRouter()


@router.get("/dashboard", response_model=DashboardReport)
def dashboard_report(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReportService.dashboard(db, current_user)


@router.get("/monthly-revenue", response_model=list[MonthlyRevenuePoint])
def monthly_revenue(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReportService.monthly_revenue(db, current_user)


@router.get("/users", response_model=list[UserReportRow])
def user_report(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReportService.user_report(db, current_user)


@router.get("/memberships", response_model=list[MembershipReportRow])
def membership_report(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReportService.membership_report(db, current_user)


@router.get("/transactions", response_model=list[TransactionReportRow])
def transaction_report(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReportService.transaction_report(db, current_user)
