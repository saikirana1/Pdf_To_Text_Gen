import PyPDF2
import io


def extract_pages(file_path):
    with open(file_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        print("Number of pages:", len(reader.pages))
        first_page = reader.pages[0].extract_text() if len(reader.pages) >= 1 else None
        second_page = reader.pages[1].extract_text() if len(reader.pages) >= 2 else None
        if first_page is None:
            print("no data found in first page")
            first_page = ""
        if second_page is None:
            print("no data found in second page")
            second_page = ""
        text = first_page + second_page
        # print(text)
        return text
