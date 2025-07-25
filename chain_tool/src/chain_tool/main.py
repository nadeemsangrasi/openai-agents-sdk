import subprocess
from dotenv import load_dotenv
from agents import set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,Agent,Runner
import os
import chainlit as cl
from typing import List
from agents.tool import function_tool
from typing import cast
import requests
set_tracing_disabled(disabled
=True)
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL_NAME")
base_url = os.getenv("BASE_URL")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.set_starters  # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",
            message="Hello! What can you help me with today?",
        ),
        cl.Starter(
            label="Weather",
            message="Find the weather in Karachi.",
        ),
    ]

@function_tool
def get_weather(city: str) -> str:
    """
    Get the weather for a given city.
    """
    # Replace with your actual weather API URL and key
    result = requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
    
    if result.status_code == 200:
        data = result.json()
        return f"The weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data."


@cl.on_chat_start
async def run():
    client = AsyncOpenAI(api_key=gemini_api_key,base_url=base_url)
    model = OpenAIChatCompletionsModel(model=model_name,openai_client=client)
    """Set up the chat session when a user connects."""
    cl.user_session.set("chat_history",[]) 
    agent= Agent(name="person, assistant",instructions="you are best personal",model=model,tools=[get_weather])
    cl.user_session.set("agent",agent)
    await cl.Message(content="Welcome to the Nadeems's Assistant").send()
@cl.on_message
async def main(message:cl.Message):
    msg = cl.Message(content="thinking...")

    await msg.send()
    agent= cast(Agent,cl.user_session.get("agent"))

    history = cl.user_session.get("chat_history") or []

    history.append({"role": "user", "content": message.content})

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result =await Runner.run(agent,str(history))

        print("\nresult\n",result.final_output,"\n")

        msg.content = result.final_output

        await msg.update()

        history.append({"role": result.last_agent.name, "content": result.final_output})

        cl.user_session.set("chat_history",history)
        print(f"User: {message.content}")
        print(f"Assistant: {result.final_output}")
        

    except Exception as e:
        print("err",e)
    

def start():
    subprocess.run(["uv","run","chainlit","run","src/chain_tool/main.py","-w"])
