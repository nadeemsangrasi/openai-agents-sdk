    
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
)


# Imports
import asyncio
import random
from typing import Any

from pydantic import BaseModel

from agents import Agent, RunContextWrapper, AgentHooks, Runner, Tool, function_tool
import os


gemini_api_key = os.getenv("GEMINI_API_KEY")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
  
class TestAgHooks(AgentHooks):
    def __init__(self, ag_display_name):
        self.event_counter = 0
        self.ag_display_name = ag_display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} started. Usage: {context.usage}")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} ended. Usage: {context.usage}, Output: {output}")
     

start_agent = Agent(
    name="Content Moderator Agent",
    instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",
    hooks=TestAgHooks(ag_display_name="content_moderator"),
    model=model
)

async def main():
  result = await Runner.run(
      start_agent,
      input=f"Will Agentic AI Die at end of 2025?."
  )

  print(result.final_output)

asyncio.run(main())
print("--end--")
     