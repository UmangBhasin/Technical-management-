from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.models.maintenance import Maintenance
from app.models.user import User
from app.schemas.maintenance import MaintenanceCreate, MaintenanceResponse, MaintenanceUpdate

router = APIRouter()


@router.post("/", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    payload: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    record = Maintenance(**payload.model_dump(), created_by=current_user.id)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/", response_model=list[MaintenanceResponse])
def list_maintenance(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.query(Maintenance).order_by(Maintenance.maintenance_date.desc()).all()


@router.put("/{record_id}", response_model=MaintenanceResponse)
def update_maintenance(
    record_id: int,
    payload: MaintenanceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    record = db.query(Maintenance).filter(Maintenance.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    for field, value in payload.model_dump().items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record
