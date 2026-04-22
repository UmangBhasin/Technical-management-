from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


ALLOWED_DURATIONS = ("6 months", "1 year", "2 years")


class MembershipCreate(BaseModel):
    member_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=8, max_length=20)
    duration: str = Field(default="6 months")
    start_date: date
    status: str = Field(default="active", pattern="^(active|inactive|suspended|cancelled)$")

    @field_validator("member_name", "phone", mode="before")
    @classmethod
    def required_text(cls, value):
        if value is None or str(value).strip() == "":
            raise ValueError("field is required")
        return value

    @field_validator("duration")
    @classmethod
    def validate_duration(cls, value: str):
        if value not in ALLOWED_DURATIONS:
            raise ValueError("duration must be one of: 6 months, 1 year, 2 years")
        return value


class MembershipActionUpdate(BaseModel):
    membership_id: int = Field(gt=0)
    action: str = Field(pattern="^(extend|cancel)$")
    extension_duration: str = Field(default="6 months")

    @field_validator("extension_duration")
    @classmethod
    def validate_extension_duration(cls, value: str):
        if value not in ALLOWED_DURATIONS:
            raise ValueError("extension_duration must be one of: 6 months, 1 year, 2 years")
        return value


class MembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_name: str
    email: EmailStr
    phone: str
    membership_type: str
    start_date: date
    end_date: date
    status: str
    id: int
    created_by: int
    created_at: datetime
