def clean_transaction_data(data):
    cleaned_data = []

    for row in data:
        withdrawal = row.get("withdrawal", "")
        if withdrawal == "" or withdrawal is None:
            withdrawal = None
        else:
            withdrawal = float(withdrawal.replace(",", ""))

        deposit = row.get("deposit", "")
        if deposit == "" or deposit is None:
            deposit = None
        else:
            deposit = float(deposit.replace(",", ""))

        balance = row.get("balance", "")
        if balance == "" or balance is None:
            balance = None
        else:
            balance = float(balance.replace(" Cr.", "").replace(",", ""))

        cleaned_row = {
            "transaction_data": row.get("transaction_data"),
            "ChequeNo": row.get("ChequeNo") or None,
            "withdrawal": withdrawal,
            "deposit": deposit,
            "balance": balance,
            "description": row.get("description"),
        }

        cleaned_data.append(cleaned_row)

    return cleaned_data
