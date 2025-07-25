# --- Imports ---
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.store.postgres.base import PoolConfig
from langmem_adapter import LangMemOpenAIAgentToolAdapter
from langmem import create_manage_memory_tool, create_search_memory_tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from agents import Agent, Runner, AsyncOpenAI, RunConfig, OpenAIChatCompletionsModel, enable_verbose_stdout_logging
from collections import deque
from models.model import UserInfo
from prompts.prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
import chainlit as cl
from typing import Optional, Dict
import asyncio, json, sys, time, os
from contextlib import asynccontextmanager
from utils.util import sanitize_username
enable_verbose_stdout_logging()

# --- Windows event loop policy ---
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- Load environment variables ---
load_dotenv()
GEMINI_KEY   = os.getenv('GEMINI_API_KEY') or (lambda: (_ for _ in ()).throw(ValueError("GEMINI_API_KEY not set")))()
EMB_MODEL    = os.getenv('EMBEDDING_MODEL', 'models/embedding-001')
PG_URL       = os.getenv("PG_URL")
BASE_URL     = os.getenv("BASE_URL")
MODEL_NAME   = os.getenv("MODEL_NAME")

os.environ['GOOGLE_API_KEY'] = GEMINI_KEY

# --- Async Store context ---
@asynccontextmanager
async def get_store():
    async with AsyncPostgresStore.from_conn_string(
        PG_URL,
        index={"dims": 768, "embed": GoogleGenerativeAIEmbeddings(model=EMB_MODEL)},
        pool_config=PoolConfig(min_size=5, max_size=100)
    ) as store:
        yield store

# --- OAuth Callback: embed username as cl.User.id ---
@cl.oauth_callback
def handle_oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_user: cl.User,
) -> Optional[cl.User]:
    # Attach the OAuth user ID directly to default_user.id
    return default_user

# --- Memory Tools Factory ---
def make_memory_tools(memory_type: str, manage_instructions: str, search_instructions: str, username: str):
    namespace = ('legal_assistant', username, memory_type)

    def create_tool(creator_func, name):
        try:
            adapter = LangMemOpenAIAgentToolAdapter(
                lambda store, namespace=None: creator_func(
                    store=store,
                    namespace=namespace,
                    instructions=manage_instructions if "manage" in name else search_instructions,
                    name=name
                ),
                store_provider=get_store,
                namespace_template=namespace
            )
            return adapter.as_tool()
        except Exception as e:
            print(f"Error creating {name}: {e}")
            return None

    return (
        create_tool(create_manage_memory_tool, f"manage_{memory_type}"),
        create_tool(create_search_memory_tool, f"search_{memory_type}")
    )

# --- WorkingMemory Class ---
class WorkingMemory:
    def __init__(self, username: str, max_msgs=10, summary_interval=5):
        self.username = username
        self.summary = ""
        self.chat_history = deque(maxlen=max_msgs)
        self.summary_interval = summary_interval
        self.message_count = 0

    def add(self, role: str, msg: str):
        self.chat_history.append({"timestamp": time.time(), "role": role, "content": msg})
        self.message_count += 1

    def should_summarize(self) -> bool:
        return self.message_count >= self.summary_interval

    def set_summary(self, text: str):
        self.summary = text
        self.message_count = 0

    def context(self) -> str:
        prefix = f"Summary: {self.summary}\n" if self.summary else ""
        body = "".join(f"{m['role'].title()}: {m['content']}\n" for m in self.chat_history)
        return prefix + body

    def save(self):
        fname = f"memory_state_{self.username}.json"
        with open(fname, "w") as f:
            json.dump({self.username: self.summary}, f)

# --- Starter Buttons ---
@cl.set_starters
async def set_starters():
    return [
        cl.Starter(label="Legal Definition", message="What is 'res judicata'?", icon="⚖️"),
        cl.Starter(label="Contract Review", message="Explain key clauses in a non-disclosure agreement.", icon="📄"),
        cl.Starter(label="Case Precedent", message="Tell me about a landmark IP case.", icon="🏛️"),
    ]

# --- Chat Start: initialize agent, memory, tools ---
@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get('user')
    username = sanitize_username( user.identifier)
    print(f"username {username}")
    
    # Initialize working memory with sanitized username
    working_memory = WorkingMemory(username=username, max_msgs=7, summary_interval=4)
    cl.user_session.set("working_memory", working_memory)

    # Create per-user memory tools
    tools = []
    for mem_type, manage_i, search_i in [
        ("semantic",   "Manage semantic legal memories...",   "Search semantic legal memories..."),
        ("episodic",   "Manage episodic legal memories...",   "Search episodic legal memories..."),
        ("procedural", "Manage procedural legal memories...", "Search procedural legal memories..."),
    ]:
        m_tool, s_tool = make_memory_tools(mem_type, manage_i, search_i, username)
        tools.extend([t for t in (m_tool, s_tool) if t])

    # Set up the agent
    client = AsyncOpenAI(api_key=GEMINI_KEY, base_url=BASE_URL, timeout=30)
    model  = OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
    config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

    agent = Agent(name="LegalAgent", instructions=SYSTEM_PROMPT, tools=tools)
    cl.user_session.set("agent", agent)
    cl.user_session.set("run_config", config)

    # Load persisted summary if any
    state_file = f"memory_state_{username}.json"
    if os.path.exists(state_file):
        with open(state_file) as f:
            state = json.load(f)
            working_memory.summary = state.get(username, "")

    await cl.Message(content="""# ⚖️ Legal AI Agent!

I'm here to help you navigate legal concepts, case histories, and procedures.

## How I can assist:

1.  **🔍 Interpret Legal Queries:** I'll understand your legal questions and needs.
2.  **🧠 Access Legal Memory:** I can retrieve definitions, statutes, case precedents, and procedural steps from my memory.
3.  **📝 Provide Clear Responses:** I'll offer concise, accurate, and relevant legal explanations.
""").send()

# --- On incoming message ---
@cl.on_message
async def on_msg(msg: cl.Message):
    user = cl.user_session.get('user')
    username = sanitize_username(user.identifier)
    print(username)
    working_memory: WorkingMemory = cl.user_session.get("working_memory")
    agent: Agent             = cl.user_session.get("agent")
    config: RunConfig        = cl.user_session.get("run_config")

    query = msg.content.strip()
    thinking_msg = await cl.Message(content="🤔 Thinking...").send()
   
    if not query:
        return await cl.Message(content="Please enter a legal query.").send()

    # Add user query to memory
    working_memory.add("user", query)

    # Summarize if needed
    if working_memory.should_summarize():
        summary_agent = Agent(name="SummaryAgent", instructions="Summarize in 2-3 sentences")
        concat_text = f"{working_memory.summary}\n" + "\n".join(
            f"{m['role']}: {m['content']}" for m in working_memory.chat_history
        )
        summary_res = await Runner.run(
            starting_agent=summary_agent,
            input=concat_text,
            run_config=config
        )
        working_memory.set_summary(summary_res.final_output)

    # Run the main legal agent
    context_blob = {"context": working_memory.context(), "timestamp": time.time()}
    result = await Runner.run(
        starting_agent=agent,
        input=f"user query: {query}\ncontext: {context_blob}",
        context=UserInfo(username=username),
        run_config=config
    )

    response = result.final_output or "(no response)"
    working_memory.add("assistant", response)
    thinking_msg.content = response
    await thinking_msg.update()


    # Persist summary-state
    working_memory.save()

def start():
    import subprocess

    subprocess.run(["uv","run","chainlit","run","src/legal_AI_Agent/main.py","-w"])






