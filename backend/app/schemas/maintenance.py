from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MaintenanceBase(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5)
    maintenance_date: date
    status: str = Field(default="planned", pattern="^(planned|in-progress|done)$")
    cost: float = Field(ge=0)


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(MaintenanceBase):
    pass


class MaintenanceResponse(MaintenanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: int
    created_at: datetime
