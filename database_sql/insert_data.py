from .database_connection import get_session

from contextlib import contextmanager
from .models import Transaction
from datetime import date, datetime


@contextmanager
def get_db_session():
    yield from get_session()


def insert_data(data):
    data2 = [
        {
            "transaction_id": None,
            "transaction_date": "30/03/2025",
            "withdrawal": None,
            "deposit": None,
            "balance": None,
            "description": "NRTGS/ICICR42025033000500805/HARVISH AGRIGENICS PV",
        },
        {
            "transaction_id": None,
            "transaction_date": "26/03/2025",
            "withdrawal": 4407.83,
            "deposit": None,
            "balance": None,
            "description": "Loan Recovery For -218920NG00000984",
        },
        {
            "transaction_id": None,
            "transaction_date": "24/03/2025",
            "withdrawal": None,
            "deposit": None,
            "balance": None,
            "description": "NEFT_IN:null//ICICN52025032400471241/SALASAR TRADING COMPAN",
        },
        {
            "transaction_id": None,
            "transaction_date": "20/03/2025",
            "withdrawal": None,
            "deposit": None,
            "balance": None,
            "description": "From:XXXX0029:STARCHIK FOODS PRIVATE LIMIT",
        },
        {
            "transaction_id": None,
            "transaction_date": "14/03/2025",
            "withdrawal": 29.5,
            "deposit": None,
            "balance": None,
            "description": "ATM ANN.CHRG FOR CARD-6615 YEAR ENDED 2024-25",
        },
        {
            "transaction_id": None,
            "transaction_date": "10/03/2025",
            "withdrawal": 44841.5,
            "deposit": None,
            "balance": None,
            "description": "NEFT_OUT:PUNBN62025031050143025/HarvishCurr/SBIN0004266/SPDCLPRJN2164",
        },
        {
            "transaction_id": None,
            "transaction_date": "07/03/2025",
            "withdrawal": None,
            "deposit": None,
            "balance": None,
            "description": "From:XXXX0029:STARCHIK FOODS PRIVATE LIMIT",
        },
        {
            "transaction_id": None,
            "transaction_date": "06/03/2025",
            "withdrawal": 7500.0,
            "deposit": None,
            "balance": None,
            "description": "IMPS_OUT/506522290604/ICIC0000245/024505005757",
        },
    ]

    with get_db_session() as session:
        for i in data:
            print(i)
            txn_date_str = i.get("transaction_data")
            txn_date = (
                datetime.strptime(txn_date_str, "%d/%m/%Y").date()
                if txn_date_str
                else None
            )
            t = Transaction(
                transaction_id=i.get("transaction_id"),
                transaction_date=txn_date,
                withdrawal=i.get("withdrawal"),
                deposit=i.get("deposit"),
                balance=i.get("balance"),
                description=i.get("description"),
            )
            session.add(t)

        session.commit()
