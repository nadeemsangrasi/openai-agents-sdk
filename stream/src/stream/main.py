import asyncio
import os
import dotenv as env
from agents.extensions.models.litellm_model import LitellmModel
from agents import Agent,Runner,function_tool,ItemHelpers,set_tracing_disabled,OpenAIChatCompletionsModel,AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
import random
env.load_dotenv(env.find_dotenv())
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME=   os.getenv("MODEL_NAME")
BASE_URL=   os.getenv("BASE_URL")


if not GEMINI_API_KEY or not MODEL_NAME:
    raise ValueError(f'{"gemini" if not GEMINI_API_KEY else "model name"} api key is not set')

set_tracing_disabled(disabled=True)

@function_tool
def jokes_count()->int:
    return random.randint(1,10)
async def main():
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url=BASE_URL,
    )

    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )
    
    # agent = Agent(
    #     name="Joker",
    #     instructions="You are a helpful assistant.",
    #     model=model

    # )

    """Streaming Text code"""
    # result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    # async for event in result.stream_events():
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #         print(event.data.delta, end="", flush=True)


    """Stream item code"""
    jokes_agent = Agent(name="jokes agent",instructions="You are a helpful assistant. First, determine how many jokes to tell, then provide jokes.",tools=[jokes_count],model=model)

    result = Runner.run_streamed(jokes_agent,input="jokes")


    async for event in result.stream_events():
        if hasattr(event, "item"):
            if event.item.type == "tool_call_output_item":
                print(f"Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(ItemHelpers.text_message_output(event.item))
        else:
            # Optionally handle or log other event types
            pass
        





def start():
    asyncio.run(main())