from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent,set_default_openai_api,set_default_openai_client,set_tracing_disabled
from agents.run import RunConfig, Runner
from dotenv import load_dotenv
import os
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
model_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
if not gemini_api_key:
     print("VARIABLE_NAME is not set.")

# model level configuration
def model_level_conf ():
    client = AsyncOpenAI(api_key=gemini_api_key,base_url=model_base_url)
    model = OpenAIChatCompletionsModel(model="gemini-2.0-flash",openai_client=client)
    agent = Agent(name="assistant",instructions="you are a helpful assistance",model=model)

    result = Runner.run_sync(agent,"hello how are u")
    print("model level conf\n",result.final_output)


# run level configuration 
# run sync
def sync():
    
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url=model_base_url
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

    agent: Agent = Agent(
        name="Assistant",
        instructions="you are a helpfull agentic ai assistant",
  
    )

    result = Runner.run_sync(agent, "what kind of asstant you are?", run_config=config)

    print("sync agent result\n",result.final_output)

# run global configuration
# run async
async def async1():
    client = AsyncOpenAI(
    base_url=model_base_url,
    api_key=gemini_api_key,
    )
    set_default_openai_client(client=client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(disabled=True)


    agent: Agent = Agent(
        name="Assistant",
        instructions="you are a helpfull agentic ai assistant",
        model="gemini-2.0-flash"
    )

    result = await Runner.run(agent, "what kind of asstant you are?")

    print("async agent result\n",result.final_output)

# run async with asycios
def async1_main():
    import asyncio
    asyncio.run(async1())


