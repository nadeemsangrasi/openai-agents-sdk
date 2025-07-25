
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY =os.getenv("OPEN_ROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

if not OPENROUTER_API_KEY:
     print("VARIABLE_NAME is not set.")


def direct_Api():
  

    response = requests.post(
    url=f"{BASE_URL}/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    },
    data=json.dumps({
        "model": MODEL,
        "messages": [
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
        ]
    })
    )

    print(response.json())
    
    data = response.json()
    data['choices'][0]['message']['content']



async def with_sdk():
    client = AsyncOpenAI(api_key=OPENROUTER_API_KEY,base_url=BASE_URL)
 
    set_tracing_disabled(disabled=True)

  
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)


    