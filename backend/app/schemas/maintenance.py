from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MaintenanceBase(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5)
    maintenance_date: date
    status: str = Field(default="planned", pattern="^(planned|in-progress|done)$")
    cost: float = Field(ge=0)

    @field_validator("title", "description")
    @classmethod
    def required_text_fields(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field is required")
        return value.strip()


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(MaintenanceBase):
    pass


class MaintenanceResponse(MaintenanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: int
    created_at: datetime
