from agents import AsyncOpenAI, Runner, Agent, OpenAIChatCompletionsModel
from agents.run import RunConfig
import os
import asyncio
import dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig
from langmem import create_manage_memory_tool, create_search_memory_tool
from langmem_adapter import LangMemOpenAIAgentToolAdapter
from typing import Optional, List, Tuple, Dict, Any
from pydantic import BaseModel
from contextlib import asynccontextmanager
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig
# Load environment variables
dotenv.load_dotenv()
import asyncio
import sys



# Environment variables
gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = str(gemini_api_key)
base_url: Optional[str] = os.getenv("BASE_URL")
model_name: Optional[str] = os.getenv("MODEL_NAME")
emb_model_name: Optional[str] = os.getenv("EMBEDDING_MODEL")
conn_string: Optional[str] = os.getenv("DATABASE_URL")

# Async context manager for Postgres store
@asynccontextmanager
async def get_store():
    async with AsyncPostgresStore.from_conn_string(
        conn_string,
        index={
            "dims": 768,
            "embed": GoogleGenerativeAIEmbeddings(model=str(emb_model_name))
        },
        pool_config=PoolConfig(
            min_size=5,
            max_size=100
        )
    ) as store:
        yield store

# Setup database migrations
async def setup_database():
    async with get_store() as store:
        await store.setup()  # Run migrations


class UserInfo(BaseModel):
  username: str

namespace=("assistant", "{username}", "collection")

# Initialize memory tools
manage_adapter = LangMemOpenAIAgentToolAdapter(
    lambda store, namespace=None: create_manage_memory_tool(namespace=namespace, store=store),
    store_provider=get_store,
    namespace_template=namespace
)
manage_memory_tool = manage_adapter.as_tool()

search_adapter = LangMemOpenAIAgentToolAdapter(
    lambda store, namespace=None: create_search_memory_tool(namespace=namespace, store=store),
    store_provider=get_store,
    namespace_template=namespace
)
search_memory_tool = search_adapter.as_tool()

# Agent system prompt
agent_system_prompt_memory: str = """
<Role>
You are Nadeem's executive assistant. You are a top-notch executive assistant who cares about AI Agents and performing as well as possible.
</Role>

<Tools>
You have access to the following tools to help manage Nadeem's communications and schedule:
1. manage_memory - Store any relevant information about contacts, actions, discussion, etc. in memory for future reference
2. search_memory - Search for any relevant information that may have been stored in memory
</Tools>
"""

async def main() -> None:
    # Setup database
    await setup_database()

    # Initialize client and model
    externel_client: AsyncOpenAI = AsyncOpenAI(
        api_key=gemini_api_key, base_url=base_url)
    model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
        model=model_name, openai_client=externel_client)
    config: RunConfig = RunConfig(
        model_provider=externel_client, model=model, tracing_disabled=True)

    # Initialize agent
    response_agent = Agent(
        name="Response agent",
        instructions=agent_system_prompt_memory,
        tools=[manage_memory_tool,search_memory_tool],
        model=model
        )


    # Conversation loop
    while True:
        query = input("me : \t")
        print("")
        if query.lower() in ["exit", "quit"]:
            break

        result: RunResult = await Runner.run(
            starting_agent=response_agent,
            input=query,
            run_config=config,
            context=UserInfo(username="nadeem"),
            
        )
        print("result : \t", result.final_output)
        print("")
        # Search stored memories
        async with get_store() as store:
            memories = await store.asearch(namespace)
            print("store : \t", memories)



def start() -> None:
    asyncio.run(main())

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    start()