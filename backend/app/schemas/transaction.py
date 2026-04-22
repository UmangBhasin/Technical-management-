from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionBase(BaseModel):
    user_id: int = Field(gt=0)
    member_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    transaction_type: str = Field(min_length=3, max_length=40)
    notes: str = Field(min_length=1, max_length=500)

    @field_validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("transaction_type is required")
        return value.strip()

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("notes is required")
        return value.strip()


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    notes: str | None = None
    id: int
    transaction_date: datetime
    created_by: int
