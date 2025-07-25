from agents import RunConfig,AsyncOpenAI,OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv
import asyncio
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.memory import InMemoryStore
from contextlib import asynccontextmanager
from langmem import create_manage_memory_tool, create_search_memory_tool
from langmem_adapter import LangMemOpenAIAgentToolAdapter  # import from your package
from models import namespace_template

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = str(gemini_api_key)

store = InMemoryStore(
      index={
          "dims": 768,
          "embed": GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
      }
    )

@asynccontextmanager
async def get_store():
  yield store



# Initialize the manage memory tool dynamically:
manage_adapter = LangMemOpenAIAgentToolAdapter(
    lambda store, namespace=None: create_manage_memory_tool(namespace=namespace, store=store),
    store_provider=get_store,
    namespace_template=namespace_template
)
manage_memory_tool = manage_adapter.as_tool()

# Initialize the search memory tool dynamically:
search_adapter = LangMemOpenAIAgentToolAdapter(
    lambda store, namespace=None: create_search_memory_tool(namespace=namespace, store=store),
    store_provider=get_store,
    namespace_template=namespace_template
)
search_memory_tool = search_adapter.as_tool()

def initialize_config()->RunConfig:
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    return RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
