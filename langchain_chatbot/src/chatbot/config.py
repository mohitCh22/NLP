from pathlib import Path
import os

from dotenv import load_dotenv

# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# Environment variables
# ---------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

API_KEY = os.getenv("API_KEY")

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gpt-4o-mini"
)

LLM_TEMPERATURE = float(
    os.getenv(
        "LLM_TEMPERATURE", 
        0.0))

LLM_TIMEOUT = float(
    os.getenv(
        "LLM_TIMEOUT", 
        30.0
    )
)

RETRIEVER_K = int(
    os.getenv(
        "RETRIEVER_K",
        4
    )
)

RETRIEVER_FETCH_K = int(
    os.getenv(
        "RETRIEVER_FETCH_K",
        "10"
    )
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment variables.")