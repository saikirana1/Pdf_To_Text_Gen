import pdfplumber
import json
from typing import List, Tuple


def _point_in_bbox(x: float, y: float, bbox: Tuple[float, float, float, float]) -> bool:
    x0, y0, x1, y1 = bbox
    return x0 <= x <= x1 and y0 <= y <= y1


def _merge_words_to_lines(words: List[dict], y_tol: float = 5.0) -> List[str]:
    """
    Merge list of words (each with 'text','top','x0') into lines using a tolerance for top coordinate.
    Assumes words are sorted by top then x0.
    """
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


def extract_plain_text_outside_tables(pdf_path: str,  y_tol: float = 5.0) -> dict:
    """
    Extract ONLY plain text that is OUTSIDE detected table bounding boxes.
    - If a page has no table boxes, the whole page text is returned.
    - If no plain text outside tables is found anywhere, an empty dict {} is written and returned.
    - Output JSON structure when content exists:
        {"plain_text": [{"page": 1, "content": "..."}, ...]}
    """
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

           

    result = {"plain_text": pages_out} if pages_out else {}

    # with open(output_json, "w", encoding="utf-8") as f:
    #     json.dump(result, f, indent=4, ensure_ascii=False)
    print(type(result))
    print(result)
    return result

