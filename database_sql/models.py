import uuid
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date


class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str


class Account(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    account_number: Optional[str] = Field(
        default_factory=lambda: str(uuid.uuid4()), index=True, unique=True
    )
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
    invoice_no: str = Field(
        default_factory=lambda: str(uuid.uuid4()), index=True, unique=True
    )
    invoice_date: Optional[date] = Field(default=None, index=True)

    items: List["Item"] = Relationship(back_populates="invoice")
    bank_details: List["BankDetails"] = Relationship(back_populates="invoice")
    sellers: List["Seller"] = Relationship(back_populates="invoice")
    payments: List["Payment"] = Relationship(back_populates="invoice")
    customers: List["Customer"] = Relationship(back_populates="invoice")


class Item(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_no: str = Field(foreign_key="invoice.invoice_no")
    item_name: Optional[str] = Field(default=None, index=True)
    hsn_code: Optional[str] = Field(default=None, index=True)
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    unit_taxable_amount: Optional[float] = None
    tax: Optional[str] = Field(default=None, index=True)
    unit_tax_amount: Optional[float] = None
    amount: Optional[float] = None
    mrp_price: Optional[float] = None

    invoice: Invoice = Relationship(back_populates="items")


class BankDetails(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_no: str = Field(foreign_key="invoice.invoice_no")
    account_number: Optional[str] = Field(default=None, index=True)
    ifsc_code: Optional[str] = Field(default=None, index=True)
    holder_name: Optional[str] = Field(default=None, index=True)
    bank_name: Optional[str] = Field(default=None, index=True)
    branch: Optional[str] = Field(default=None, index=True)

    invoice: Invoice = Relationship(back_populates="bank_details")


class Seller(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_no: str = Field(foreign_key="invoice.invoice_no")
    address: Optional[str] = Field(default=None, index=True)
    contact: Optional[str] = Field(default=None, index=True)
    gst_number: Optional[str] = Field(default=None, index=True)
    fssai_no: Optional[str] = Field(default=None, index=True)
    pin_code: Optional[str] = Field(default=None, index=True)

    invoice: Invoice = Relationship(back_populates="sellers")


class Payment(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_no: str = Field(foreign_key="invoice.invoice_no")
    sub_total: Optional[float] = Field(default=None, index=True)
    s_gst: Optional[float] = Field(default=None, index=True)
    c_gst: Optional[float] = Field(default=None, index=True)
    discount: Optional[float] = Field(default=None, index=True)
    total: Optional[float] = Field(default=None, index=True)

    invoice: Invoice = Relationship(back_populates="payments")


class Customer(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    invoice_no: str = Field(foreign_key="invoice.invoice_no")
    name: Optional[str] = Field(default=None, index=True)
    address: Optional[str] = Field(default=None, index=True)
    gst_number: Optional[str] = Field(default=None, index=True)
    invoice: Invoice = Relationship(back_populates="customers")
