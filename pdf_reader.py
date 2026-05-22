import os
from pypdf import PdfReader


def read_all_pdfs(folder_path="pdfs"):
    pdf_text = ""

    if not os.path.exists(folder_path):
        print("PDF folder not found")
        return ""

    for filename in os.listdir(folder_path):

        if filename.endswith(".pdf"):

            file_path = os.path.join(folder_path, filename)

            print(f"Reading PDF: {filename}")

            try:
                reader = PdfReader(file_path)

                for page in reader.pages:
                    text = page.extract_text()

                    if text:
                        pdf_text += text + "\n"

                print(f"{filename} loaded successfully")

            except Exception as e:
                print(f"Error reading {filename}: {e}")

    return pdf_text