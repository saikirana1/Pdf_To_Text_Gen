from .database_connection import get_session
from pinecone_v_db.insert_records import insert_records
from contextlib import contextmanager
from .models import Transaction,Account,Invoice,Item
from datetime import date, datetime
from sqlmodel import select

@contextmanager
def get_db_session():
    yield from get_session()


def insert_invoice_data(data ):
    # pine_data=insert_records(data)
 with get_db_session() as session:
    records = data.get("result", [])
    if not records:
        return "no data found"

    first_record = records[0]

    invoice_no = first_record.get("invoice_no")
    invoice_date_val = first_record.get("invoice_date")
    if isinstance(invoice_date_val, str):
        invoice_date = datetime.strptime(invoice_date_val, "%Y-%m-%d").date()
    elif isinstance(invoice_date_val, datetime):
        invoice_date = invoice_date_val.date()
    elif isinstance(invoice_date_val, date):  
        invoice_date = invoice_date_val
    else:
        invoice_date = None
    
    invoice = session.exec(
            select(Invoice).where(Invoice.invoice_no == invoice_no)
          ).first()

    if not invoice:
        invoice = Invoice(
            invoice_no=invoice_no,
            invoice_date=invoice_date,
        )
        session.add(invoice)
        session.commit()
        session.refresh(invoice)

        for record in records:

            item = Item(
                invoice_no=invoice.invoice_no,
                item_name=record.get("item_name"),
                quantity=record.get("quantity"),
                unit_price=record.get("unit_price"),
                unit_taxable_amount=record.get("unit_taxable_amount"),
                tax=record.get("tax"),
                unit_tax_amount=record.get("unit_tax_amount"),
                amount=record.get("amount"),
                mrp_price=record.get("mrp_price"),
                gst_number=record.get("gst_number"),
            )


            session.add(item)

        session.commit()

        
