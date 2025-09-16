from .database_connection import get_session

from contextlib import contextmanager
from .models import Transaction,Account,Invoice,Item
from datetime import date, datetime


@contextmanager
def get_db_session():
    yield from get_session()


def insert_data(data):

    with get_db_session() as session:
        #data={'account': [{'account_number': '2189050000480', 'ifsc_code': 'PUNB0218920', 'name': 'HARVISH AGRIGENICS PRIVATE LIMITED'}], 'transactions': [{'transaction_id': None, 'transaction_date': '2025-03-30', 'withdrawal': None, 'deposit': None, 'balance': None, 'description': 'NRTGS/ICICR42025033000500805/HARVISH AGRIGENICS PV', 'check_number': None}, {'transaction_id': None, 'transaction_date': '2025-03-26', 'withdrawal': 4407.83, 'deposit': None, 'balance': None, 'description': 'Loan Recovery For -218920NG00000984', 'check_number': None}, {'transaction_id': None, 'transaction_date': '2025-03-24', 'withdrawal': None, 'deposit': None, 'balance': None, 'description': 'NEFT_IN:null//ICICN52025032400471241/SALASAR TRADING COMPANY', 'check_number': None}, {'transaction_id': None, 'transaction_date': '2025-03-20', 'withdrawal': None, 'deposit': None, 'balance': None, 'description': 'From:XXXX0029:STARCHIK FOODS PRIVATE LIMIT', 'check_number': None}, {'transaction_id': None, 'transaction_date': '2025-03-14', 'withdrawal': 29.5, 'deposit': None, 'balance': None, 'description': 'ATM ANN.CHRG FOR CARD-6615 YEAR ENDED 2024-25', 'check_number': None}, {'transaction_id': None, 'transaction_date': '2025-03-10', 'withdrawal': None, 'deposit': 44841.5, 'balance': None, 'description': 'NEFT_OUT:PUNBN62025031050143025/HarvishCurr/SBIN0004266/SPDCLPRJN2164', 'check_number': None}, {'transaction_id': None, 'transaction_date': '2025-03-07', 'withdrawal': None, 'deposit': None, 'balance': None, 'description': 'From:XXXX0029:STARCHIK FOODS PRIVATE LIMIT', 'check_number': None}, {'transaction_id': None, 'transaction_date': '2025-03-06', 'withdrawal': 7500.0, 'deposit': None, 'balance': None, 'description': 'IMPS\ufffeOUT/506522290604/ICIC0000245/024505005757', 'check_number': None}]}
        
        account_data = data["account"][0]

        account = Account(
            account_number=account_data["account_number"],
            ifsc_code=account_data.get("ifsc_code"),
            name=account_data.get("name"),
        )

        session.add(account)
        session.commit()  
        session.refresh(account)


        for txn in data.get("transactions", []):
            txn_date_str = txn.get("transaction_date")
            txn_date = (
                datetime.strptime(txn_date_str, "%Y-%m-%d").date()
                if txn_date_str
                else None
            )

            transaction = Transaction(
                transaction_id=txn.get("transaction_id"),
                transaction_date=txn_date,
                withdrawal=txn.get("withdrawal"),
                deposit=txn.get("deposit"),
                balance=txn.get("balance"),
                description=txn.get("description"),
                check_number=txn.get("check_number"),
                account_number=account.account_number, 
            )

            session.add(transaction)

        session.commit()

        
