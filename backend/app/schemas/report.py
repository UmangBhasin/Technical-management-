from pydantic import BaseModel


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
