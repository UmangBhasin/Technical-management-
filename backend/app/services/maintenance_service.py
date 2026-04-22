from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate


class MaintenanceService:
    @staticmethod
    def create(db: Session, payload: MaintenanceCreate, user_id: int) -> Maintenance:
        record = Maintenance(**payload.model_dump(), created_by=user_id)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def list_all(db: Session) -> list[Maintenance]:
        return db.query(Maintenance).order_by(Maintenance.maintenance_date.desc()).all()

    @staticmethod
    def update(db: Session, record_id: int, payload: MaintenanceUpdate) -> Maintenance:
        record = db.query(Maintenance).filter(Maintenance.id == record_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Maintenance record not found")

        for field, value in payload.model_dump().items():
            setattr(record, field, value)

        db.commit()
        db.refresh(record)
        return record
