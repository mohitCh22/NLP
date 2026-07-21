from marshal import load
import os

# from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv

from .prompt import system_prompt, user_prompt

import httpx

# if not os.getenv("GROQ_API_KEY"):
#     raise RuntimeError("GROQ_API_KEY is not set")

load_dotenv()

# _client = Groq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     http_client=httpx.Client(
#         verify=False,
#         timeout=30.0,   # important
#     ),
# )
_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # your existing key
    http_client=httpx.Client(
        verify=False,  # bypass Zscaler SSL
        timeout=30.0,
    ),
)


def call_llama_api(query, context):
    # client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    formatted_prompt = user_prompt.format(context=context, query=query)
    print("=" * 50)
    print("USER PROMPT SENT TO OPENAI:")
    print("=" * 50)
    print(formatted_prompt)
    print("=" * 50)
    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": formatted_prompt,
            },
        ],
    )
    return response.choices[0].message.content
