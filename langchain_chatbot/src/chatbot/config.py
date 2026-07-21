from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
INDEX_DIR = ARTIFACTS_DIR / "indexes"

RAW_PDF_PATH = RAW_DATA_DIR / "CPA2019.pdf"
EXTRACTED_TEXT_PATH = PROCESSED_DATA_DIR / "CPA2019.txt"
SECTIONS_TEXT_PATH = PROCESSED_DATA_DIR / "sections.txt"
SECTIONS_JSON_PATH = PROCESSED_DATA_DIR / "sections_debug.json"
FAISS_INDEX_PATH = INDEX_DIR / "cpa_index.faiss"

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

FAISS_PATH = INDEX_DIR / "cpa_index.faiss"
JSON_PATH = PROCESSED_DATA_DIR / "sections_debug.json"

print("Configuration loaded:")