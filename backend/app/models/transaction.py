from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("memberships.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(40), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    # Requested naming aliases without breaking existing fields.
    transaction_id = synonym("id")
    user_id = synonym("created_by")
    date = synonym("transaction_date")

    creator = relationship("User", back_populates="transactions")
    user = relationship("User", foreign_keys=[created_by], viewonly=True)
    member = relationship("Membership", back_populates="transactions")
