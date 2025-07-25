from dotenv import load_dotenv,find_dotenv
from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled
import asyncio

#model level config

# Load environment variables from a .env file
load_dotenv(find_dotenv())

import os

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
BASE_URL= os.getenv("BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
client = AsyncOpenAI(api_key=OPEN_ROUTER_API_KEY,base_url=BASE_URL)
set_tracing_disabled(disabled=True)
async def main():
    agent = Agent(name="my personal assistance",instructions="you are personal assistant of Nadeem Khan",model=OpenAIChatCompletionsModel(model=MODEL_NAME,openai_client=client))
    history = []
    isChatStart=True
    while isChatStart:
        query = input("me :\t")
        if query.lower() == "quit":
            isChatStart=False
            print("history",history)
            break
        if len(history):
            query = f"this is user query : {query}\nand this prevouse chat with this user{history} note:when ever I ask about what said last or what was my last prompt so you will tell me only user query"
        result = await Runner.run(agent,query)
        history.append({"user":query,"assistant":result.final_output})
        print("AI : ",result.final_output)


def start():
    asyncio.run(main())


