from pathlib import Path
import re

from pypdf import PdfReader

from .config import EXTRACTED_TEXT_PATH, RAW_PDF_PATH

def extract_content_from_pdf(pdf_file_path: str | Path = RAW_PDF_PATH) -> str:
    text = ""
    with open(pdf_file_path, "rb") as pdf_file:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            page_content = page.extract_text()
            if page_content:
                text += page_content + "\n"
    return text

def save_txt_file(
    txt_file_path: str | Path = EXTRACTED_TEXT_PATH,
    pdf_file_path: str | Path = RAW_PDF_PATH,
) -> str:
    text = extract_content_from_pdf(pdf_file_path)
    clean = re.sub(r'[^A-Za-z0-9IVXLCDMivxlcdm()\[\]\s]+', '', text)
    txt_file_path = Path(txt_file_path)
    txt_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(clean)
    print(f"Text successfully saved to {txt_file_path}\n")
    return str(txt_file_path)

