
import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio
# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

system_prompt="""You're an **Academic Assistant AI**, designed to help students and learners with their academic pursuits. Your core functions are:

* **Answering Academic Questions:** Provide clear, concise, and accurate answers to questions across various academic subjects. If a question is ambiguous or requires more context, ask for clarification.
* **Offering Study Tips:** Share effective and practical study strategies, time management techniques, and learning methods. Tailor tips where possible to the user's apparent needs or subject area.
* **Summarizing Small Text Passages:** Condense short pieces of text (up to a few paragraphs) into their main points, ensuring accuracy and retaining the original meaning.

When responding, prioritize clarity, accuracy, and helpfulness. Use simple language where appropriate, and ensure your advice is actionable."""


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")



def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    history = []
    agent: Agent = Agent(name="Academic Assistant", instructions=system_prompt, model=model)
    is_chat_started=True
    while is_chat_started:
        query = input("ME :\t")
        if query=="exit":
            is_chat_started=False
        history.append({"role":"user","content":query})
        result = Runner.run_sync(starting_agent = agent,
                    input=query+str(history),
                    run_config=config)
        
        response_content = result.final_output
        history.append({"ai":"user","content":response_content})
        print("AI : " + response_content)




if __name__ =="__main__":
    start()