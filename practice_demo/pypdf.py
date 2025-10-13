import PyPDF2

def extract_text_from_pdf(pdf_path):

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)  
        print("Number of pages:", len(reader.pages))
        first_page_data = reader.pages[0]
        second_page = reader.pages[1]
        second_page_data=second_page.extract_text()
        text = first_page_data.extract_text()
        total_data=text+second_page_data
        return total_data