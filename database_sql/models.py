import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date


class Account(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    account_number: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), index=True, unique=True)
    ifsc_code: Optional[str] = Field(default=None, index=True)
    name: Optional[str] = Field(default=None, index=True)

    transactions: List["Transaction"] = Relationship(back_populates="account")


class Transaction(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    transaction_id: Optional[str] = Field(default=None, index=True)
    transaction_date: Optional[date] = Field(default=None, index=True)
    withdrawal: Optional[float] = None
    deposit: Optional[float] = None
    balance: Optional[float] = None
    description: Optional[str] = Field(default=None, index=True)
    check_number: Optional[str] = Field(default=None, index=True)

    account_number: str = Field(foreign_key="account.account_number")  
    account: Optional[Account] = Relationship(back_populates="transactions")


class Invoice(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_no: Optional[str] = Field(default=None, index=True, unique=True)
    invoice_date: Optional[date] = Field(default=None, index=True)

    items: List["Item"] = Relationship(back_populates="invoice")


class Item(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_no: str = Field(foreign_key="invoice.invoice_no")   
    item_name: Optional[str] = Field(default=None, index=True)
    quantity: Optional[float] = None
    unit_price: Optional[float] = None   
    unit_taxable_amount: Optional[float] = None
    tax: Optional[str] = Field(default=None, index=True)
    unit_tax_amount: Optional[float] = None
    amount: Optional[float] = None
    invoice: Optional[Invoice] = Relationship(back_populates="items")
