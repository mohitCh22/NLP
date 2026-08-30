import asyncio
import os
import httpx
from src.chatbot.config import API_KEY

URL = "http://127.0.0.1:8000/api/v1/chat"


async def send_request(client, request_number):

    response = await client.post(
        URL,
        headers={
            "X-API-Key": API_KEY
        },
        json={
            "question": f"Who is cosumer {request_number}?"
        }
    )

    print(
        f"Request {request_number}: "
        f"status={response.status_code}"
    )


async def main():

    async with httpx.AsyncClient() as client:

        tasks = [
            send_request(client, i)
            for i in range(1, 11)
        ]

        await asyncio.gather(*tasks)


asyncio.run(main())