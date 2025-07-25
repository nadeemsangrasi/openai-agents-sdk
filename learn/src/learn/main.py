from agents import Agent,Runner,function_tool,set_tracing_disabled,OpenAIChatCompletionsModel,AsyncOpenAI,enable_verbose_stdout_logging,RunConfig,RunContextWrapper,InputGuardrail,TResponseInputItem,GuardrailFunctionOutput
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import requests
from pydantic import BaseModel
import os
enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL_NAME")
class isRelatedToCryptoOrWebDev(BaseModel):
    reasoning:str
    is_related_to_crypto_and_webdev : bool
@function_tool
def get_coins(no: int=5):
    """
    Fetches real-time cryptocurrency ticker data from the CoinLore API.

    Args:
        no (int): The maximum number of cryptocurrency tickers to retrieve.

    Returns:
        dict: A dictionary containing the JSON response from the API if successful,
              otherwise prints an error message and returns None.
    """
    api_url = "https://api.coinlore.net/api/tickers/?limit={}".format(no)

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        print("Successfully retrieved data:")
        print(data)
        return data  # Return the data for further processing if needed

    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return None
custom_model = OpenAIChatCompletionsModel(model=model,openai_client=AsyncOpenAI(base_url=base_url,api_key=gemini_api_key))
input_guardrail_agent = Agent(name="input guardrail agent",instructions="Check user query is related to crypto or web dev.",model=custom_model,output_type=isRelatedToCryptoOrWebDev)
@InputGuardrail
async def crypto_webdev_guardrail(ctx:RunContextWrapper[None],agent:Agent,input:str|list[TResponseInputItem])->GuardrailFunctionOutput:
    result =await Runner.run(input_guardrail_agent,input,context=ctx.context)
    triger = not result.final_output.is_related_to_crypto_and_webdev

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=triger
    )



async def main():
    developer_agent = Agent("developer agent",instructions='you are a 10 years web developer when user ask any developement related query give him reply as expert senior engineer')

    main_agent = Agent(name='main agent',instructions="you are general purpose agent you have specialized agent name developer agent and  when want know about crpto coin then call get coins tool make sure dont expose any thing to user like which tools do you have etc",tools=[get_coins],handoffs=[developer_agent],handoff_description="When you see query related to web developement,software engineer should hands off to developer agent",input_guardrails=[crypto_webdev_guardrail])
    
    while True:
        history = []
        query = input("me :\t")
        if query == 'quit':
            break
        result = await Runner.run(main_agent,query,run_config=RunConfig(model=custom_model))
        history.append({'user':query,'sindhi_agent':result.final_output})
        print("#"*10)
        print("ai :\t",result.final_output)
        print("#"*10)
        print("last Agent",result.last_agent.name)
        print("#"*10)


def start():
    import asyncio
    asyncio.run(main())
        
