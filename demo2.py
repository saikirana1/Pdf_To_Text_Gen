# import pdfplumber
# import re
# import json
# from datetime import datetime


# def parse_transactions(text):
#     transactions = []
#     # Split into lines
#     lines = text.splitlines()

#     for line in lines:
#         # Example regex for: txn_id, value_date, posted_date, description, txn_type, amount, balance
#         match = re.match(
#             r"([S\d]+)\s+(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}\s+(?:AM|PM))(.+?)(CR|DR)(\d+\.\d+)(\d+\.\d+)",
#             line,
#         )

#         if match:
#             txn_id = match.group(1).strip()
#             value_date = datetime.strptime(match.group(2), "%d/%m/%Y").strftime(
#                 "%Y-%m-%d"
#             )
#             posted_date = datetime.strptime(
#                 match.group(3), "%d/%m/%Y %I:%M:%S %p"
#             ).strftime("%Y-%m-%d %H:%M:%S")
#             description = match.group(4).strip()
#             txn_type = match.group(5).strip()
#             amount = float(match.group(6))
#             balance = float(match.group(7))

#             transactions.append(
#                 {
#                     "txn_id": txn_id,
#                     "value_date": value_date,
#                     "posted_date": posted_date,
#                     "description": description,
#                     "txn_type": txn_type,
#                     "amount": amount,
#                     "balance": balance,
#                 }
#             )

#     return transactions


# def pdf_to_json(pdf_path, output_json="transactions.json"):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"

#     transactions = parse_transactions(text)
#     print(text)
#     # Save as JSON
#     with open(output_json, "w") as f:
#         json.dump(transactions, f, indent=2)

#     return transactions


# if __name__ == "__main__":
#     pdf_file = "bank.pdf"  # replace with your PDF file
#     transactions = pdf_to_json(pdf_file, "transactions.json")

#     print("✅ Extracted Transactions:")
#     print(json.dumps(transactions, indent=2))


# import pdfplumber

# with pdfplumber.open("bank.pdf") as pdf:
#     for i, page in enumerate(pdf.pages):
#         text = page.extract_text()
#         print(f"--- Page {i + 1} ---")
#         print(text)

#         # Extract tables
#         tables = page.extract_tables()
#         for table in tables:
#             for row in table:
#                 print(row)


# import pdfplumber
# import pandas as pd
# import json

# pdf_path = "bank.pdf"
# all_rows = []
# headers = None

# with pdfplumber.open(pdf_path) as pdf:
#     for page in pdf.pages:
#         tables = page.extract_tables()
#         for table in tables:
#             if not headers:
#                 headers = table[0]  # take first row as headers
#             for row in table[1:]:
#                 # Clean up newlines and spaces
#                 cleaned_row = [
#                     cell.replace("\n", " ").strip() if cell else "" for cell in row
#                 ]
#                 all_rows.append(cleaned_row)
#                 print(row)
#             print(all_rows)

# # Convert to DataFrame
# df = pd.DataFrame(all_rows, columns=[col.replace("\n", " ").strip() for col in headers])

# # Save DataFrame to JSON
# json_data = df.to_dict(orient="records")

# # Write to file
# with open("transactions.json", "w", encoding="utf-8") as f:
#     json.dump(json_data, f, indent=4, ensure_ascii=False)

# print("✅ PDF data stored in transactions.json")


# from transformers import DonutProcessor, VisionEncoderDecoderModel
# from PIL import Image
# import torch
# import fitz  # pymupdf
# import json

# # Load pretrained model
# processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
# model = VisionEncoderDecoderModel.from_pretrained(
#     "naver-clova-ix/donut-base-finetuned-docvqa"
# )

# # Open PDF page as image
# doc = fitz.open("bank_statement.pdf")
# page = doc[0].get_pixmap()
# img = Image.frombytes("RGB", [page.width, page.height], page.samples)

# # Encode input
# pixel_values = processor(img, return_tensors="pt").pixel_values
# decoder_input_ids = processor.tokenizer(
#     "<s>", add_special_tokens=False, return_tensors="pt"
# ).input_ids

# # Generate output
# outputs = model.generate(
#     pixel_values, decoder_input_ids=decoder_input_ids, max_length=512
# )
# result = processor.tokenizer.decode(outputs[0], skip_special_tokens=True)

# # Convert result (string) to valid JSON
# try:
#     data = json.loads(result)  # parse JSON string
# except json.JSONDecodeError:
#     # if result is not valid JSON, wrap it in a dict
#     data = {"raw_output": result}

# # Save JSON file
# with open("bank_statement.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, indent=4, ensure_ascii=False)

# print("✅ JSON file saved as bank_statement.json")


# from open_ai.pdf_to_json_data_extract import pdf_to_json_data_extract, client


# with open("p-1.pdf", "rb") as f:
#     uploaded_file = client.files.create(file=f, purpose="user_data")

# t = pdf_to_json_data_extract(uploaded_file)
# print(t)


# from database_sql.create_table import create_db_and_tables

# from database_sql.insert_data import insert_data


# t = insert_data()

# print(t)


# t = create_db_and_tables()
# print(t)


# import pdfplumber
# import pandas as pd
# import json


# def pdf_to_json(pdf_path, output_json, table_headers):
#     all_rows = []

#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             tables = page.extract_tables()
#             for table in tables:
#                 for row in table[1:]:  # skip PDF headers
#                     cleaned_row = [
#                         cell.replace("\n", " ").strip() if cell else "" for cell in row
#                     ]
#                     all_rows.append(cleaned_row)

#     # Use the headers you provided
#     df = pd.DataFrame(all_rows, columns=table_headers)

#     json_data = df.to_dict(orient="records")

#     with open(output_json, "w", encoding="utf-8") as f:
#         json.dump(json_data, f, indent=4, ensure_ascii=False)

#     print(f"✅ PDF data stored in {output_json}")


# # Example usage
# my_headers = [
#     "transaction_data",
#     "ChequeNo",
#     "withdrawal",
#     "deposit",
#     "balance",
#     "description",
# ]

# pdf_to_json("p_bank.pdf", "transactions4.json", my_headers)


import pdfplumber
import pandas as pd
import json


def pdf_to_json(pdf_path, output_json, table_headers, skip_columns=None):
    all_rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table[1:]:  # skip PDF headers
                    cleaned_row = [
                        cell.replace("\n", " ").strip() if cell else "" for cell in row
                    ]
                    all_rows.append(cleaned_row)

    # Create DataFrame
    df = pd.DataFrame(all_rows, columns=table_headers)

    # Drop columns if specified
    if skip_columns:
        df = df.drop(
            columns=skip_columns, errors="ignore"
        )  # 'ignore' avoids errors if column not found

    # Convert to JSON
    json_data = df.to_dict(orient="records")

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    print(f"✅ PDF data stored in {output_json} (skipped columns: {skip_columns})")


# Example usage
my_headers = [
    "transaction_data",
    "ChequeNo",
    "withdrawal",
    "deposit",
    "balance",
    "Narration",
]

# Skip "ChequeNo" column
pdf_to_json(
    "p_bank.pdf",
    "transactions6.json",
    my_headers,
    skip_columns=["ChequeNo", "Narration"],
)
