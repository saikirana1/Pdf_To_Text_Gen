from .database_connection import get_session
from pinecone_v_db.insert_ice_cream_data import insert_ice_cream_data
from contextlib import contextmanager
from .models import Invoice, Item, Payment, BankDetails, Customer, Seller
from datetime import date, datetime
from sqlmodel import select

@contextmanager
def get_db_session():
    yield from get_session()


def insert_invoice_data(data):
    print("i am process started======--------------->")
    records = data.get("result", [])
    if not records:
        print("No data-------------------------")
        return "No data found"

    with get_db_session() as session:
        for record in records:
            print("--------------->", record)
            invoice_no = record.get("invoice_no")
            invoice_date_val = record.get("invoice_date")
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
            for item_data in record.get("items", []):
                print("item_data------------------->", item_data)
                item = Item(
                    invoice_no=invoice.invoice_no,
                    item_name=item_data.get("item_name"),
                    hsn_code=item_data.get("hsn_code"),
                    quantity=item_data.get("quantity"),
                    unit_price=item_data.get("unit_price"),
                    unit_taxable_amount=item_data.get("unit_taxable_amount"),
                    tax=item_data.get("tax"),
                    unit_tax_amount=item_data.get("unit_tax_amount"),
                    amount=item_data.get("amount"),
                    mrp_price=item_data.get("mrp_price"),
                )
                session.add(item)

            for bank_data in record.get("bank_details", []):
                print("bank_data----------------------->", bank_data)
                bank = BankDetails(
                    invoice_no=invoice.invoice_no,
                    account_number=bank_data.get("account_number"),
                    ifsc_code=bank_data.get("ifsc_code"),
                    holder_name=bank_data.get("holder_name"),
                    bank_name=bank_data.get("bank_name"),
                    branch=bank_data.get("branch"),
                )
                session.add(bank)

            for seller_data in record.get("sellers", []):
                print("seller_data --------------------->", seller_data)
                seller = Seller(
                    invoice_no=invoice.invoice_no,
                    address=seller_data.get("address"),
                    contact=seller_data.get("contact"),
                    gst_number=seller_data.get("gst_number"),
                    fssai_no=seller_data.get("fssai_no"),
                    pin_code=seller_data.get("pin_code"),
                )
                session.add(seller)

            for payment_data in record.get("payments", []):
                print("payment----------->", payment_data)
                payment = Payment(
                    invoice_no=invoice.invoice_no,
                    sub_total=payment_data.get("sub_total"),
                    s_gst=payment_data.get("s_gst"),
                    c_gst=payment_data.get("c_gst"),
                    discount=payment_data.get("discount"),
                    total=payment_data.get("total"),
                )
                session.add(payment)
            for customer_data in record.get("customers", []):
                print("customer_data-------------------->", customer_data)
                customer = Customer(
                    invoice_no=invoice.invoice_no,
                    name=customer_data.get("name"),
                    address=customer_data.get("address"),
                    gst_number=customer_data.get("gst_number"),
                )
                session.add(customer)

            session.commit()
    insert_ice_cream_data(data)
    return "Data inserted successfully"