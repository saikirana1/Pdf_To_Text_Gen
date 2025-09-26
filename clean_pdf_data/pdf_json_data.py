import pdfplumber
import pandas as pd
import json


def pdf_to_json(pdf_path,  skip_columns=None):
    all_rows = []
    headers = None 

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue

               
                if headers is None:
                    raw_headers = table[0]
                    headers = [
                        cell.replace("\n", " ").strip() if cell else ""
                        for cell in raw_headers
                    ]
                
              
                for row in table[1:]:
                    cleaned_row = [
                        cell.replace("\n", " ").strip() if cell else "" for cell in row
                    ]
                    
                    if any("Date" in h for h in cleaned_row) or all(c == "" for c in cleaned_row):
                        continue
                    all_rows.append(cleaned_row)

   
    if all_rows and headers:
        df = pd.DataFrame(all_rows, columns=headers[: len(all_rows[0])])
    else:
        df = pd.DataFrame()

    
    if skip_columns:
        df = df.drop(columns=skip_columns, errors="ignore")

 
    json_data = df.to_dict(orient="records")

    
    result=json.dumps(json_data,  indent=4)

    print(type(result))
    print(result)
    print(type(result))
    return result


