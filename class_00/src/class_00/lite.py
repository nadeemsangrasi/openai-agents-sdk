from agents import Agent,Runner,AsyncOpenAI,set_tracing_disabled
from dotenv import find_dotenv,load_dotenv
from agents.extensions.models.litellm_model import LitellmModel
import os
load_dotenv(find_dotenv())

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")


set_tracing_disabled(disabled=True)

# client = AsyncOpenAI
agent = Agent(name="Cloud Teacher",instructions="you are 10 year exprienced cloud teacher",model=LitellmModel(api_key=GEMINI_API_KEY,model=MODEL_NAME))

result = Runner.run_sync(agent,"hellow who are you")
print("result",result.final_output)

