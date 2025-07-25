from agents import AsyncOpenAI, Runner, Agent, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.result import RunResult
import os
import asyncio
import dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool
from langmem_adapter import LangMemOpenAIAgentToolAdapter
from typing import Optional, List, Tuple, Dict, Any
from pydantic import BaseModel

from contextlib import asynccontextmanager
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig

dotenv.load_dotenv()
gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = str(gemini_api_key)
base_url: Optional[str] = os.getenv("BASE_URL")
model_name: Optional[str] = os.getenv("MODEL_NAME")
emb_model_name: Optional[str] = os.getenv("EMBEDDING_MODEL")
postgress_str: Optional[str] = os.getenv("POSTGRESS_STR")

store: InMemoryStore = InMemoryStore(
    index={
        "dims": 786,
        "embed": GoogleGenerativeAIEmbeddings(model=str(emb_model_name))
    }
)

namespace: Tuple[str, str] = ("assistant", "collection")


adapter: LangMemOpenAIAgentToolAdapter = LangMemOpenAIAgentToolAdapter(
    create_manage_memory_tool(namespace=namespace, store=store)
)
call_manage_memory_tool: Dict[str, Any] = adapter.as_tool()

search_memory_tool_adapter: LangMemOpenAIAgentToolAdapter = LangMemOpenAIAgentToolAdapter(
    create_search_memory_tool(namespace=namespace, store=store)
)
call_search_memory_tool: Dict[str, Any] = search_memory_tool_adapter.as_tool()


agent_system_prompt_memory: str = """
< Role >
You are Nadeem executive assistant. You are a top-notch executive assistant who cares about AI Agents and performing as well as possible.
 Role >

< Tools >
You have access to the following tools to help manage Junaid's communications and schedule:

1. manage_memory - Store any relevant information about contacts, actions, discussion, etc. in memory for future reference
2. search_memory - Search for any relevant information that may have been stored in memory
 Tools >
"""


async def main() -> None:
    externel_client: AsyncOpenAI = AsyncOpenAI(
        api_key=gemini_api_key, base_url=base_url)
    model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
        model=model_name, openai_client=externel_client)
    config: RunConfig = RunConfig(
        model_provider=externel_client, model=model, tracing_disabled=True)

    agent: Agent = Agent(
        name="Assistant",
        instructions=agent_system_prompt_memory,
        tools=[call_manage_memory_tool, call_search_memory_tool]
    )

    while True:

        query = input("me : \t")
        print("")
        if query in ["exit","quit"]:
            break

        result: RunResult = await Runner.run(
            starting_agent=agent,
            input=query,
            run_config=config,
        )
        print("result : \t", result.final_output)
        print("")
        print("store \t",store.search(namespace))








def start() -> None:
    asyncio.run(main())
