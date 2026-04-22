from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    member_id: int
    amount: float = Field(gt=0)
    transaction_type: str = Field(min_length=3, max_length=40)
    notes: str | None = Field(default=None, max_length=500)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    transaction_date: datetime
    created_by: int
