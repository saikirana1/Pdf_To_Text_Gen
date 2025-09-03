from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
import uuid
from datetime import date


class Transaction(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    transaction_id: Optional[str] = Field(default=None, index=True)
    transaction_date: Optional[date] = Field(default=None, index=True)
    withdrawal: Optional[float] = None
    deposit: Optional[float] = None
    balance: Optional[float] = None
    description: Optional[str] = None
