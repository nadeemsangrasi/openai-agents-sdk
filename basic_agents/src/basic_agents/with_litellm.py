from agents.extensions.models.litellm_model import LitellmModel
from agents import Agent,Runner,function_tool
import os
from dotenv import load_dotenv
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
     print("VARIABLE_NAME is not set.")


def start():
    @function_tool
    def get_real_time_news(topic:str):
        return f"news about {topic} is here"

    model = LitellmModel(model="gemini-2.0-flash",api_key=gemini_api_key)
    agent = Agent(name="news agent",instructions="you are a news agent and you have news fetching tool whenever user ask about news you will call it",model=model,tools=[get_real_time_news])
    user_query = input("Ask what you want?")
    result = Runner.run_sync(agent,user_query)
    print("answer",result.final_output)

start()
