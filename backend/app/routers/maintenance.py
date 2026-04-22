from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_admin
from app.models.user import User
from app.schemas.maintenance import MaintenanceCreate, MaintenanceResponse, MaintenanceUpdate
from app.schemas.user import UserMaintenanceCreate, UserMaintenanceUpdate, UserResponse
from app.services.maintenance_service import MaintenanceService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=MaintenanceResponse, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    payload: MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return MaintenanceService.create(db, payload, current_user.id)


@router.get("/", response_model=list[MaintenanceResponse])
def list_maintenance(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return MaintenanceService.list_all(db)


@router.put("/{record_id}", response_model=MaintenanceResponse)
def update_maintenance(
    record_id: int,
    payload: MaintenanceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return MaintenanceService.update(db, record_id, payload)


@router.get("/users", response_model=list[UserResponse])
def list_users_for_maintenance(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return UserService.list_users(db)


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_for_maintenance(
    payload: UserMaintenanceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return UserService.create_user_from_maintenance(db, payload)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_for_maintenance(
    user_id: int,
    payload: UserMaintenanceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return UserService.update_user_from_maintenance(db, user_id, payload)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_for_maintenance(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    UserService.delete_user_from_maintenance(db, user_id, current_user.id)
