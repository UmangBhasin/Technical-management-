import calendar
from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.membership import Membership
from app.schemas.membership import MembershipActionUpdate, MembershipCreate


class MembershipService:
    @staticmethod
    def _duration_to_months(duration: str) -> int:
        mapping = {
            "6 months": 6,
            "1 year": 12,
            "2 years": 24,
        }
        return mapping[duration]

    @staticmethod
    def _add_months(base_date: date, months: int) -> date:
        month_index = base_date.month - 1 + months
        year = base_date.year + month_index // 12
        month = month_index % 12 + 1
        last_day = calendar.monthrange(year, month)[1]
        day = min(base_date.day, last_day)
        return date(year, month, day)

    @staticmethod
    def create(db: Session, payload: MembershipCreate, user_id: int) -> Membership:
        end_date = MembershipService._add_months(payload.start_date, MembershipService._duration_to_months(payload.duration))
        membership = Membership(
            member_name=payload.member_name,
            email=payload.email,
            phone=payload.phone,
            membership_type=payload.duration,
            start_date=payload.start_date,
            end_date=end_date,
            status=payload.status,
            created_by=user_id,
        )
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership

    @staticmethod
    def list_all(db: Session) -> list[Membership]:
        return db.query(Membership).order_by(Membership.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, membership_id: int) -> Membership:
        membership = db.query(Membership).filter(Membership.id == membership_id).first()
        if not membership:
            raise HTTPException(status_code=404, detail="Membership not found")
        return membership

    @staticmethod
    def update(db: Session, membership_id: int, payload: MembershipActionUpdate) -> Membership:
        if payload.membership_id != membership_id:
            raise HTTPException(status_code=400, detail="membership_id in payload must match URL membership_id")

        membership = MembershipService.get_by_id(db, membership_id)

        if payload.action == "cancel":
            membership.status = "cancelled"
        else:
            extend_months = MembershipService._duration_to_months(payload.extension_duration)
            membership.end_date = MembershipService._add_months(membership.end_date, extend_months)
            membership.membership_type = payload.extension_duration
            if membership.status == "cancelled":
                membership.status = "active"

        db.commit()
        db.refresh(membership)
        return membership
