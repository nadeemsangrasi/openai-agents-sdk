
from pydantic import BaseModel, Field
from agents import (
    Agent,
    Runner
)
import asyncio
from typing import Dict, Any
from typing_extensions import TypedDict, Literal, Annotated
import os
from dotenv import load_dotenv
from config import initialize_config,search_memory_tool,manage_memory_tool,get_store,store
from utils import create_prompt,profile,prompt_instructions,email_input,format_few_shot_examples 
from prompts import triage_system_prompt_template,triage_user_prompt_template,response_prompt_template
from models import Router,Email,Triple,UserInfo
from tools import *
from langmem import create_memory_manager #
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Configure extraction
manager = create_memory_manager(
    "google_genai:gemini-2.0-flash",
    schemas=[Triple],
    instructions="Extract user preferences and any other useful information",
    enable_inserts=True,
    enable_deletes=True,
)

config = initialize_config()

# system_prompt = create_prompt(triage_system_prompt_template, {
#     "full_name": profile["full_name"],
#     "name":profile["name"],
#     "examples": None,
#     "user_profile_background": profile["user_profile_background"],
#     "triage_no" : prompt_instructions["triage_rules"]["ignore"],
#     "triage_notify": prompt_instructions["triage_rules"]["notify"],
#     "triage_email" : prompt_instructions["triage_rules"]["respond"] ,
#   }
# )


# First conversation - extract triples
# conversation1 = [
#     {"role": "user", "content": "We are building AI Agents to make Mars next humans stop"}
# ]
# memories = manager.invoke({"messages": conversation1})
# print("After first conversation:")
# for m in memories:
#     print(m)

# # Second conversation - update and add triples
# conversation2 = [
#     {"role": "user", "content": "Junaid AI Agents Workspace can now suggest designs for AI Agents Core."}
# ]
# update = manager.invoke({"messages": conversation2, "existing": memories})
# print("After second conversation:")
# for m in update:
#     print(m)

# existing = [m for m in update if isinstance(m.content, Triple)]

async def main():
    username= profile['name']
    namespace = (
        "email_assistant",
        username,
        "examples"
    )

    examples = store.search(
        namespace,
        query=str({"email": email_input}),
    )
    examples=format_few_shot_examples(examples)

    system_prompt = create_prompt(triage_system_prompt_template, {
        "full_name": profile["full_name"],
        "name":profile["name"],
        "user_profile_background": profile["user_profile_background"],
        "triage_no" : prompt_instructions["triage_rules"]["ignore"],
        "triage_notify": prompt_instructions["triage_rules"]["notify"],
        "triage_email" : prompt_instructions["triage_rules"]["respond"],
        "examples": examples,
      }
    )
    
    triage_agent = Agent(
        name="Triage Agent",
        instructions=system_prompt,
        output_type=Router
    )
        
    
    response_system_prompt = create_prompt(response_prompt_template, {
        "full_name": profile["full_name"],
        "name":profile["name"],
        "instructions": prompt_instructions["agent_instructions"] +  "Always save my email interactions in memory store for later discussions.",
    }
    )
    response_agent = Agent(
    name="Response agent",
    instructions=response_system_prompt,
tools=[write_email, schedule_meeting, check_calendar_availability, manage_memory_tool, search_memory_tool],
tool_use_behavior=
    )

    await triage_router(email_input,profile['name'],triage_agent,response_agent)



async def triage_router(email: Email, username: str,triage_agent,response_agent):

    user_prompt = create_prompt(triage_user_prompt_template, {
      "author": email['from'],
      "to": email['to'],
      "subject": email['subject'],
      "email_thread" : email['body']
    })

    triage_result = await Runner.run(
        triage_agent,
        user_prompt,
        run_config = config,
        context=UserInfo(username=username)
        )

    print(triage_result.final_output)
    print("Triage History: ", triage_result.to_input_list())
    async with get_store() as store:
        namespace=("email_assistant", profile["name"], "collection")
        res = await store.asearch(namespace)
        print(res)

    if triage_result.final_output.classification == "respond":
          print("📧 Classification: RESPOND - This email requires a response")
          
          response_result = await Runner.run(
              response_agent,
              f"Respond to the email {email.model_dump_json(by_alias=True)}",
              run_config = config,
              context=UserInfo(username=username)
              )
          print(response_result.final_output)
          print("Response History", response_result.to_input_list())
    elif triage_result.final_output.classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
    elif triage_result.final_output.classification == "notify":
        # If real life, this would do something else
        print("🔔 Classification: NOTIFY - This email contains important information")
    else:
        raise ValueError(f"Invalid classification: {triage_result.final_output.classification}")

     

def start():
    asyncio.run(main())
