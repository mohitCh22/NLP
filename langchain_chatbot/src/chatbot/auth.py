import secrets

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from src.chatbot.config import API_KEY

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if not API_KEY:
        raise RuntimeError("API_KEY is not configured")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )

    if not secrets.compare_digest(api_key, API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return True