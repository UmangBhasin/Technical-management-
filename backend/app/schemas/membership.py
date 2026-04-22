from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class MembershipBase(BaseModel):
    member_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=8, max_length=20)
    membership_type: str = Field(min_length=3, max_length=40)
    start_date: date
    end_date: date
    status: str = Field(default="active", pattern="^(active|inactive|suspended)$")

    @field_validator("end_date")
    @classmethod
    def validate_dates(cls, value: date, values):
        start_date = values.data.get("start_date")
        if start_date and value < start_date:
            raise ValueError("end_date must be on or after start_date")
        return value


class MembershipCreate(MembershipBase):
    pass


class MembershipUpdate(MembershipBase):
    pass


class MembershipResponse(MembershipBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_by: int
    created_at: datetime
