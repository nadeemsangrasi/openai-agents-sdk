from dotenv import load_dotenv
import os
from collections import deque
from langgraph.store.memory import InMemoryStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from contextlib import asynccontextmanager
from pydantic import BaseModel
from langmem_adapter import LangMemOpenAIAgentToolAdapter
from langmem import create_manage_memory_tool, create_search_memory_tool
from agents import AsyncOpenAI, RunConfig, OpenAIChatCompletionsModel, Runner, Agent, function_tool
import asyncio
import time
import json

# ---------------------------
# Environment & Store Setup
# ---------------------------
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
emb_model = os.getenv('EMBEDDING_MODEL', "models/embedding-001")

if not gemini_api_key:
    raise ValueError('GEMINI_API_KEY not found in environment')

os.environ['GOOGLE_API_KEY'] = gemini_api_key

# Create embedding model instance
embeddings = GoogleGenerativeAIEmbeddings(model=emb_model)

store = InMemoryStore(index={
    'dims': 768,
    'embed': embeddings
})

@asynccontextmanager
async def get_store():
    try:
        yield store
    finally:
        pass  # Add any cleanup logic here

# ---------------------------
# Enhanced Working Memory
# ---------------------------
class WorkingMemory:
    def __init__(self, max_messages: int = 10, summary_interval: int = 5):
        self.summary: str = ""
        self.chat_history: deque = deque(maxlen=max_messages)
        self.max_messages = max_messages
        self.summary_interval = summary_interval
        self.message_count = 0

    def add_message(self, role: str, content: str):
        """Add message with role metadata"""
        self.chat_history.append({
            "timestamp": time.time(),
            "role": role,
            "content": content
        })
        self.message_count += 1

    def set_summary(self, new_summary: str):
        """Update conversation summary"""
        self.summary = new_summary
        # Reset counter after summarization
        self.message_count = 0

    def should_summarize(self) -> bool:
        """Check if summarization should be triggered"""
        return self.message_count >= self.summary_interval

    def get_context(self) -> str:
        """Get formatted context for agent"""
        context = f"Conversation Summary: {self.summary}\n" if self.summary else ""
        context += "Recent Messages:\n"
        for msg in self.chat_history:
            context += f"{msg['role'].capitalize()}: {msg['content']}\n"
        return context

    def save_history(self, filename: str = "conversation_history.json"):
        """Persist conversation history"""
        with open(filename, 'w') as f:
            json.dump(list(self.chat_history), f, indent=2)

    def clear(self):
        self.summary = ""
        self.chat_history.clear()
        self.message_count = 0

# Initialize with configurable summarization
working_memory = WorkingMemory(max_messages=7, summary_interval=4)

# ---------------------------
# Pydantic Schemas (Optimized)
# ---------------------------
class Triple(BaseModel):
    subject: str
    predicate: str
    object: str
    context: str | None = None

class InteractionLog(BaseModel):
    event: str
    details: str
    timestamp: float = time.time()

class Workflow(BaseModel):
    name: str
    steps: list[str]
    completed: bool = False
    last_updated: float = time.time()

class UserInfo(BaseModel):
    username: str
    user_id: str | None = None

# ---------------------------
# Memory Tools Factory (Enhanced)
# ---------------------------
def make_memory_tools(
    memory_type: str,
    manage_instructions: str,
    search_instructions: str,
):
    namespace = ('dev_assistant', '{username}', memory_type)

    # Create tool with error handling
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
            print(f"Error creating {name}: {str(e)}")
            return None

    manage_tool = create_tool(create_manage_memory_tool, f'manage_{memory_type}')
    search_tool = create_tool(create_search_memory_tool, f'search_{memory_type}')
    
    return manage_tool, search_tool

# Create tools with error handling
try:
    manage_semantic, search_semantic = make_memory_tools(
        'semantic',
        'Manage semantic memories: software knowledge, definitions, and concepts',
        'Search semantic memories for technical concepts and definitions'
    )
    
    manage_episodic, search_episodic = make_memory_tools(
        'episodic',
        'Manage episodic memories: personal development experiences and project history',
        'Search episodic memories for past experiences and solutions'
    )
    
    manage_procedural, search_procedural = make_memory_tools(
        'procedural',
        'Manage procedural memories: step-by-step instructions and best practices',
        'Search procedural memories for how-to guides and workflows'
    )
except Exception as e:
    print(f"Critical error initializing memory tools: {str(e)}")
    exit(1)

# ---------------------------
# Agent & Tools Setup (Improved)
# ---------------------------
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
    timeout=30  # Add timeout
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=client,
    
)

config = RunConfig(model=model, model_provider=client, tracing_disabled=True)

@function_tool
def save_conversation(filename: str = "conversation_backup.json") -> str:
    """Save current conversation to file"""
    working_memory.save_history(filename)
    return f"Conversation saved to {filename}"

SYSTEM_PROMPT = """
You are an AI development assistant with memory capabilities. Use these guidelines:

1. Memory Types:
   - SEMANTIC: General knowledge (concepts, definitions)
   - EPISODIC: Personal experiences (past solutions, project history)
   - PROCEDURAL: Step-by-step instructions (how-tos, workflows)

2. Tool Selection:
   a) SEARCH when:
      - User asks factual questions (semantic)
      - User references past experiences (episodic)
      - User requests procedures (procedural)
   
   b) MANAGE when:
      - User provides information worth remembering
      - Explicitly asked to remember something

3. Response Requirements:
   - Always check working memory first
   - Use tools for memory operations
   - Explain your reasoning briefly
   - Keep responses concise but complete

4. Special Cases:
   - For "summary" commands: Use built-in summarization
   - For "save" commands: Use save_conversation tool
   - For "exit/quit": Shutdown gracefully

Working memory contains: {context}
"""

# Create agent with all tools
agent_tools = [
    tool for tool in [
        save_conversation,
        manage_semantic,
        search_semantic,
        manage_episodic,
        search_episodic,
        manage_procedural,
        search_procedural
    ] if tool is not None  # Filter out failed tools
]

agent = Agent(
    name='DevAssistant',
    instructions=SYSTEM_PROMPT,
    tools=agent_tools
)

# ---------------------------
# Main Interactive Loop (Enhanced)
# ---------------------------
async def main():
    print("Developer Assistant initialized. Type 'exit' or 'quit' to end session.")
    
    # Conversation persistence
    try:
        if os.path.exists("memory_state.json"):
            with open("memory_state.json", "r") as f:
                state = json.load(f)
                working_memory.summary = state.get("summary", "")
                print(f"Loaded previous conversation summary")
    except Exception as e:
        print(f"Couldn't load state: {str(e)}")

    while True:
        try:
            # Check for summarization trigger
            if working_memory.should_summarize():
                print("\n[Summarizing conversation...]")
                summary_agent = Agent(
                    name="SummaryAgent",
                    instructions="Condense conversation history into 2-3 sentence summary. Maintain technical context."
                )
                
                summary_input = (
                    f"Current Summary: {working_memory.summary}\n"
                    f"New Messages:\n" + "\n".join(
                        f"{msg['role']}: {msg['content']}" 
                        for msg in list(working_memory.chat_history)[-working_memory.summary_interval:]
                    )
                )
                
                result = await Runner.run(
                    starting_agent=summary_agent,
                    input=summary_input,
                    run_config=config
                )
                
                working_memory.set_summary(result.final_output)
                print(f"Summary Updated: {result.final_output[:80]}...")

            # Get user input
            query = input('\nYou: ')
            if query.lower() in ['exit', 'quit']:
                print("Shutting down...")
                working_memory.save_history()
                break

            # Add to working memory
            working_memory.add_message("user", query)
            
            # Prepare agent context
            context = {
                "context": working_memory.get_context(),
                "timestamp": time.time()
            }
            
            # Execute agent
            result = await Runner.run(
                starting_agent=agent,
                input=query,
                context=UserInfo(username='Nadeem'),
                run_config=config
            )
            
            # Handle agent response
            if result.final_output:
                working_memory.add_message("assistant", result.final_output)
                print(f"\nAssistant: {result.final_output}")
            else:
                print("\nAssistant: (No response generated)")

        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except Exception as e:
            print(f"\nSystem Error: {str(e)}")
            # Attempt to save state on critical error
            working_memory.save_history(f"error_backup_{int(time.time())}.json")
            print("Conversation state saved. Please restart.")

    # Final persistence
    with open("memory_state.json", "w") as f:
        json.dump({"summary": working_memory.summary}, f)

# ---------------------------
# Execution Improvements
# ---------------------------
def start():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSession terminated")
    finally:
        print("Cleanup complete")

if __name__ == '__main__':
    start()