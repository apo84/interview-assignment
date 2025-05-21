import fitz  # PyMuPDF
import os
from typing import List

# Extracts text from each page of the given PDF.
# Args: Path to the PDF file. 
# Return: List of strings, where each string is the text from one page.

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    #Support for user, returns pdf file options if incorrect path is prompted
    if not os.path.isfile(pdf_path):
        available_files = [f for f in os.listdir(os.path.dirname(pdf_path) or '.') if f.lower().endswith('.pdf')]
        raise FileNotFoundError(
            f"File not found: {pdf_path}\nAvailable PDF files in the directory:\n" + '\n'.join(available_files)
        )

    doc_text = [] #List of pdf page information
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text = page.get_text()
                doc_text.append(text)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from {pdf_path}: {str(e)}")

    return doc_text

#When testing method
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python parser.py path/to/pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    pages = extract_text_from_pdf(pdf_path)

    for i, text in enumerate(pages):
        print(f"\n--- Page {i+1} ---\n{text}")