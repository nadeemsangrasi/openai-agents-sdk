from marketaura.utils import initialize_env_variables,sanitize_username
from agents import Agent,Runner,RunConfig,enable_verbose_stdout_logging,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from marketaura.prompts import traige_agent_system_prompt,general_purpose_system_prompt,crypto_agent_system_prompt
from marketaura.tools import get_coins_id_by_names,getAllCoinsTool,getAllExchanges,getCoinsByIDs,getExchangesByIds,marketDataForCoins,socialStatsTool
from contextlib import asynccontextmanager
from langgraph.store.postgres import AsyncPostgresStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.postgres.base import PoolConfig
from langmem_adapter import LangMemOpenAIAgentToolAdapter
from langmem import create_manage_memory_tool, create_search_memory_tool
from collections import deque
import json,time,os,asyncio,sys
import chainlit as cl
from typing import Dict,Optional
from pydantic import BaseModel

set_tracing_disabled(disabled=True)
# --- Windows event loop policy ---
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

enable_verbose_stdout_logging()
model_name,gemini_api_key,base_url,embedding_model,db_url = initialize_env_variables()
os.environ['GOOGLE_API_KEY'] = gemini_api_key


@asynccontextmanager
async def get_store():
    async with AsyncPostgresStore.from_conn_string(
        db_url,
        index={"dims": 768, "embed": GoogleGenerativeAIEmbeddings(model=embedding_model)},
        pool_config=PoolConfig(min_size=5,max_size=100)
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

def make_memory_tools(agent_name:str,memory_type: str, manage_instructions: str, search_instructions: str, username: str):  
    namespace = (agent_name,username,memory_type)

    def create_tool(creator_func,name):
        try:
            adapter = LangMemOpenAIAgentToolAdapter(
                lambda store,namespace=None:creator_func(
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

class WorkingMemory():
    def __init__(self,username,max_msgs=10,summary_interval=5):
        self.username = username
        self.summary = ""
        self.chat_history = deque(maxlen=max_msgs)
        self.summary_interval = summary_interval
        self.message_count = 0

    def add(self,role:str,msg:str):
        self.chat_history.append({'timestamps':time.time(),'role':role,'content':msg})
        self.message_count+=1
    
    def should_summary(self)->bool:
        return self.message_count >= self.summary_interval
    
    def save_summary(self,text):
        self.summary=text
        self.message_count=0
        
    def get_context(self): 
        prefix = f"Summary : {self.summary}" if self.summary else ""
        body = "".join(f"{m['role'].title()}: {m['content']}\n" for m in self.chat_history)
        return prefix+body
    
    def save(self): 
        fname = f"memory_state_{self.username}.json"
        with open(fname, "w") as f:
            json.dump({self.username: self.summary}, f)

class UserInfo(BaseModel):
    username : str 

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(label="Coin Compaire", message="What is 'Future Trading?", icon="🔮"),
        cl.Starter(label="Market data", message="Explain key element in trading", icon="👾"),
        cl.Starter(label="Exchange", message="Tell me about a BTC And Eth ", icon="🪙"),
    ]
        


@cl.on_chat_start
async def on_chat_start():
    user = cl.user_session.get("user")
    username  = sanitize_username(user.identifier)
    print(f"username {username}")

    # Initialize working memory with sanitized username
    working_memory = WorkingMemory(username=username, max_msgs=7, summary_interval=4)
    cl.user_session.set("working_memory", working_memory)

    client = AsyncOpenAI(api_key=gemini_api_key,base_url=base_url)
    model = OpenAIChatCompletionsModel(model=model_name,openai_client=client)
    config = RunConfig(model=model,tracing_disabled=True,model_provider=client)

    general_purpose_agent_tools = []
    crypto_agent_tools = [getAllCoinsTool,getAllExchanges,getCoinsByIDs,getExchangesByIds,marketDataForCoins,socialStatsTool]
    for mem_type, manage_i, search_i in [
        ("semantic",   "Manage semantic general memories...",   "Search semantic general memories..."),
        ("episodic",   "Manage episodic general memories...",   "Search episodic general memories..."),
        ("procedural", "Manage procedural general memories...", "Search procedural general memories..."),
    ]:
        m_tool, s_tool = make_memory_tools("general_purpose_agent",mem_type, manage_i, search_i, username)
        general_purpose_agent_tools.extend([t for t in (m_tool, s_tool) if t])
    for mem_type, manage_i, search_i in [
        ("semantic",   "Manage semantic crypto related memories...",   "Search semantic crypto related memories..."),
        ("episodic",   "Manage episodic crypto related memories...",   "Search episodic crypto related memories..."),
        ("procedural", "Manage procedural crypto related memories...", "Search procedural crypto related memories..."),
    ]:
        m_tool, s_tool = make_memory_tools("crypto_agent_tools",mem_type, manage_i, search_i, username)
        crypto_agent_tools.extend([t for t in (m_tool, s_tool) if t])

    general_purpose_agent =Agent(name="General Purpose Agent",instructions=general_purpose_system_prompt,tools=general_purpose_agent_tools) 
    crypto_agent = Agent(name="Crypto Agent",instructions=crypto_agent_system_prompt,tools=crypto_agent_tools)
    triage_agent = Agent(name="Triage Agent",instructions=traige_agent_system_prompt,tools=[get_coins_id_by_names],handoffs=[general_purpose_agent,crypto_agent])
    cl.user_session.set("triage_agent",triage_agent)
    cl.user_session.set("config",config)
    cl.user_session.set("username",username)

        # Load persisted summary if any
    state_file = f"memory_state_{username}.json"
    if os.path.exists(state_file):
        with open(state_file) as f:
            state = json.load(f)
            working_memory.summary = state.get(username, "")

        await cl.Message(content="""# Crypto AI Agent!
## How I can assist:

1.  **🔍 Interpret crypto Queries:** I'll understand your crypto questions and needs.
2.  **🧠 Access crypto Memory:** I can retrieve definitions, statutes, case precedents, and procedural steps from my memory.
3.  **📝 Provide Clear Responses:** I'll offer concise, accurate, and relevant crypto explanations, enriched with **realtime market data and social stats**.
""").send()

@cl.on_message
async def on_msg(msg:cl.Message):
    triage_agent = cl.user_session.get("triage_agent")
    config = cl.user_session.get("config")
    working_memory:WorkingMemory = cl.user_session.get("working_memory")
    username = cl.user_session.get('username')

    query = msg.content.strip()
    thinking_msg = await cl.Message(content="🤔 Thinking...").send()

    working_memory.add("user",query)

    if working_memory.should_summary():
        summary_agent = Agent(name="summary_agents",instructions="Summarize in 2-3 sentences")
        concat_text = f"{working_memory.summary}\n" + "\n".join(
            f"{m['role']}: {m['content']}" for m in working_memory.chat_history
        )
        summary_res = await Runner.run(
            starting_agent=summary_agent,
            input=concat_text,
            run_config=config
        )
        working_memory.save_summary(summary_res.final_output)
 

    # Run the main legal agent
    context_blob = {"context": working_memory.get_context(), "timestamp": time.time()}
    result = await Runner.run(
        starting_agent=triage_agent,
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

    subprocess.run(["uv","run","chainlit","run","src/marketaura/main.py","-w"])
