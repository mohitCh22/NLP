import logging
import uuid
import time

from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel, Field

from src.chatbot.auth import verify_api_key

from slowapi import Limiter
from slowapi.util import get_remote_address
from src.chatbot.rate_limit import limiter


logger  = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/api/v1",
    tags = ["chat"]
)

# Controlling the request format to be as the chat endpoint
class ChatRequest(BaseModel):
    question:str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The question to ask the AI model."
    )

class ChatResponse(BaseModel):
    request_id:str
    question:str
    answer:str
    sources:list[dict]
    latency_in_seconds:float

@router.post("/chat",response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
async def chat(request:Request,body:ChatRequest):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "Chat request received | request_id=%s", request_id
    )

    try:
        chain = request.app.state.chain

        result = await chain.ainvoke(body.question)

        latency = time.perf_counter() - start_time

        sources = [ 
            {
                "section": doc.metadata.get("section"),
                "subsection": doc.metadata.get("subsection"),
                "content_preview": doc.page_content[:300]  # Preview first 200 characters
            }
            for doc in result["source_documents"]
            ]

        logger.info(
            "Chat request processed | request_id=%s | latency=%.3f seconds", request_id, latency
        )

        return ChatResponse(
            request_id=request_id,
            question=body.question,
            answer=result["answer"],
            sources=sources,
            latency_in_seconds=round(latency, 3)
        )

    except Exception:

        latency = time.perf_counter() - start_time

        logger.exception(
            "Chat request failed | request_id=%s | latency=%.3f seconds", request_id, latency
        )

        raise HTTPException(status_code=500, 
                            detail = {
            "message": "An error occurred while processing the request.",
            "request_id": request_id
        }
        )