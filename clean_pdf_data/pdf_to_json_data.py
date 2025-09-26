import pdfplumber
import pandas as pd
import json
from typing import List, Tuple


# ------------------- Helpers -------------------
def _point_in_bbox(x: float, y: float, bbox: Tuple[float, float, float, float]) -> bool:
    x0, y0, x1, y1 = bbox
    return x0 <= x <= x1 and y0 <= y <= y1


def _merge_words_to_lines(words: List[dict], y_tol: float = 5.0) -> List[str]:
    lines = []
    current_line = []
    current_top = None

    for w in words:
        top = float(w["top"])
        if current_top is None or abs(top - current_top) > y_tol:
            if current_line:
                lines.append(" ".join([ww["text"] for ww in current_line]))
            current_line = [w]
            current_top = top
        else:
            current_line.append(w)

    if current_line:
        lines.append(" ".join([ww["text"] for ww in current_line]))

    return lines


# ------------------- Extract Tables -------------------
def extract_tables_from_pdf(pdf_path: str, skip_columns=None) -> list:
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

    return df.to_dict(orient="records")


# ------------------- Extract Plain Text Outside Tables -------------------
def extract_plain_text_outside_tables(pdf_path: str, y_tol: float = 5.0) -> list:
    pages_out = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            table_bboxes: List[Tuple[float, float, float, float]] = []
            for tbl in page.find_tables():
                try:
                    bbox = tbl.bbox
                    if bbox:
                        table_bboxes.append(bbox)
                except Exception:
                    continue

            if not table_bboxes:
                text = page.extract_text()
                if text and text.strip():
                    pages_out.append({"page": page_number, "content": text.strip()})
                continue

            words = page.extract_words()
            outside_words: List[dict] = []
            for w in words:
                try:
                    mid_x = (float(w["x0"]) + float(w["x1"])) / 2.0
                    mid_y = (float(w["top"]) + float(w["bottom"])) / 2.0
                except Exception:
                    continue

                inside_any = False
                for bbox in table_bboxes:
                    if _point_in_bbox(mid_x, mid_y, bbox):
                        inside_any = True
                        break
                if not inside_any:
                    outside_words.append(w)

            if outside_words:
                outside_words_sorted = sorted(outside_words, key=lambda x: (float(x["top"]), float(x["x0"])))
                lines = _merge_words_to_lines(outside_words_sorted, y_tol=y_tol)
                content = "\n".join(line.strip() for line in lines if line.strip())
                if content:
                    pages_out.append({"page": page_number, "content": content})

    return pages_out


# ------------------- Combined Function -------------------
def pdf_to_combined_json(pdf_path: str, skip_columns=None) -> dict:
    tables = extract_tables_from_pdf(pdf_path, skip_columns=skip_columns)
    plain_text = extract_plain_text_outside_tables(pdf_path)

    result = {
        "transaction_data": tables if tables else [],
        "account_data": plain_text if plain_text else []
    }

    # Print result
    final_result=json.dumps(result, indent=4, ensure_ascii=False)
    print(final_result)
    return result


# ------------------- Example Usage ------------------
