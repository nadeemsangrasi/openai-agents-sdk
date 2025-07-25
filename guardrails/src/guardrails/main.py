from dotenv import load_dotenv
from agents import set_tracing_disabled,Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,input_guardrail,RunContextWrapper,TResponseInputItem,GuardrailFunctionOutput,RunConfig,output_guardrail,InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered
from pydantic import BaseModel
import os
import asyncio
import chainlit as cl
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY") 
base_url = os.getenv("BASE_URL") 
model_name = os.getenv("MODEL_NAME") 

if not gemini_api_key:
    raise ValueError("GEMINI API KEY NOT FOUND")

if not base_url:
    raise ValueError("BASE URL NOT FOUND")

if not model_name:
    raise ValueError("MODEL NAME NOT FOUND")



new_client = AsyncOpenAI(api_key=gemini_api_key,base_url=base_url)
model = OpenAIChatCompletionsModel(model=model_name,openai_client=new_client)
google_gemini_config = RunConfig(
    model=model,
    model_provider=new_client,
    tracing_disabled=True
)
class isCloudQuery(BaseModel):
    reasoning:str
    is_related_to_cloud:bool
guardrail_agent  = Agent(name="Guardrail check", instructions="Check if the user is asking you query is related to cloud and devOps",output_type=isCloudQuery)

@input_guardrail
async def cloud_check_guard(ctx:RunContextWrapper[None],agent:Agent,input : str | list[TResponseInputItem])->GuardrailFunctionOutput:
     result = await Runner.run(guardrail_agent,input,context=ctx,run_config=google_gemini_config) 
     tiger = not result.final_output.is_related_to_cloud
     return GuardrailFunctionOutput(
         output_info=result.final_output,
         tripwire_triggered=tiger
     )
class CheckResponse(BaseModel):
    reasoning:str
    is_related_to_cloud:bool
guardrail_agent2 = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any cloud and devops.",
    output_type=CheckResponse,
)
@output_guardrail
async def cloud_check_response(ctx:RunContextWrapper[None],agent:Agent,input : str | list[TResponseInputItem])->GuardrailFunctionOutput:
     result = await Runner.run(guardrail_agent2,input,context=ctx,run_config=google_gemini_config) 
     tiger = not result.final_output.is_related_to_cloud
     return GuardrailFunctionOutput(
         output_info=result.final_output,
         tripwire_triggered=tiger
     )


async def main():
   
    try:
        cloud_and_devops_engineer =Agent(name="cloud and devOps engineer",instructions="your are 10 years experienced cloud and devops engineer who are specialized in cloud architecture and application deployments strategies you will only respond to cloud and devops related stuff",input_guardrails=[cloud_check_guard],output_guardrails=[cloud_check_response])

        while True:
            query = input("me : \t:")
            if query in ['quit',"exit"]:
                break 
            result = await Runner.run(cloud_and_devops_engineer,input=query,run_config=google_gemini_config) 
            print("ai : \t" + str(result.final_output))
    except OutputGuardrailTripwireTriggered as e:
        print("error",e)
    except InputGuardrailTripwireTriggered as e:
        print("error",e)
        
asyncio.run(main())