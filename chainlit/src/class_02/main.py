import sys
import subprocess
import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


@cl.on_chat_start
async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
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
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)
    developer_agent: Agent = Agent(name="Software developer Agent", instructions="You are a software developer agent which answer the programming and software developement quries", model=model)
    teacher_agent: Agent = Agent(name="Teacher Agent", instructions="You are a 10 year exprience collage teacher you will be responsible for collage level or school level studies question answers", model=model)
    triage_agent: Agent = Agent(name="Triage Agent", instructions="You are a triage agent. If the user query is related to college studies or programming, you will route (handoff) the query to a specialized agent. If the query is not related to these topics, you will answer it yourself.", model=model,handoffs=[developer_agent,teacher_agent])

    cl.user_session.set("triage_agent", triage_agent)
 

    await cl.Message(content="Welcome to ").send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    triage_agent :Agent= cast (Agent,cl.user_session.get("triage_agent"))


    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(starting_agent = triage_agent,
                    input=str(history),
                    run_config=config)
        
       

        response_content = result.final_output
        
        # Do this:
        history.append({
            "role": result.last_agent.name,
            "content": response_content
        })
        # Optionally, log or store agent info elsewhere if needed
        
        # Update the session with the new history.
        cl.user_session.set("chat_history", history)
        print()
        print("history",history,end="")
        print()

        msg = cl.Message(content=response_content)
        await msg.send()
        
        
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")

def main():

    subprocess.run(["uv", "run", "chainlit", "run", "src/class_02/main.py", "-w"])

if __name__ == "__main__":
    main()