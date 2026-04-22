from pydantic import BaseModel
from datetime import date, datetime


class DashboardReport(BaseModel):
    total_users: int
    total_memberships: int
    active_memberships: int
    total_transactions: int
    total_revenue: float
    total_maintenance_cost: float


class MonthlyRevenuePoint(BaseModel):
    month: str
    revenue: float


class UserReportRow(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime


class MembershipReportRow(BaseModel):
    id: int
    member_name: str
    email: str
    membership_type: str
    start_date: date
    end_date: date
    status: str


class TransactionReportRow(BaseModel):
    id: int
    user_id: int
    user_name: str
    member_name: str
    amount: float
    transaction_type: str
    transaction_date: datetime
