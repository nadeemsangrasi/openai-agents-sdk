import os
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
from langmem import (
    create_memory_manager,
    create_memory_store_manager,
    create_manage_memory_tool,
    create_search_memory_tool,
    create_prompt_optimizer,
    create_multi_prompt_optimizer
)
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.store.memory import InMemoryStore

load_dotenv()
MODEL = "google_genai:gemini-2.0-flash"
gemini_api_key = os.getenv("GEMINI_API_KEY")

# --- Section A: Basic Memory Manager Usage ---
async def demo_basic_memory_manager():
    print("\n--- Basic Memory Manager Demo ---\n")
    preference_conversation = [
        {"role": "user", "content": "I prefer dark mode in all my apps"},
        {"role": "assistant", "content": "I'll remember that preference"},
    ]
    manager = create_memory_manager(MODEL)
    memories = await manager.ainvoke({"messages": preference_conversation})
    print("[MEM]", memories)
    print(memories[0][1])

# --- Section B: Custom Store Usage ---
class PreferenceMemory(BaseModel):
    """Store preferences about the user."""
    category: str
    preference: str
    context: str

async def demo_custom_store():
    print("\n--- Custom Store Demo ---\n")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    store = InMemoryStore(
        index={
            "dims": 768,
            "embed": embeddings,
        }
    )
    manager = create_memory_store_manager(
        MODEL,
        schemas=[PreferenceMemory],
        namespace=("AI-201", "{panaversity_user_id}"),
        store=store
    )
    conversation = [
        {"role": "user", "content": "I prefer dark mode in all my apps"},
        {"role": "assistant", "content": "I'll remember that preference"}
    ]
    await manager.ainvoke(
        {"messages": conversation},
        config={"configurable": {"panaversity_user_id": "user123"}}
    )
    print("\nStored memories:")
    memories = store.search(("AI-201", "user123"))
    for memory in memories:
        print(f"\nMemory {memory.key}:")
        print(f"Content: {memory.value['content']}")
        print(f"Kind: {memory.value['kind']}")

# --- Section C: Memory Tool Usage ---
def demo_memory_tool():
    print("\n--- Memory Tool Demo ---\n")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    store = InMemoryStore(
        index={
            "dims": 768,
            "embed": embeddings,
        }
    )
    namespace = ("project_memories", "memory")
    memory_tool = create_manage_memory_tool(
        namespace=namespace,
        store=store
    )
    print(type(memory_tool))
    print(memory_tool)
    # Search tool
    search_memory_tool = create_search_memory_tool(
        namespace=namespace,
        store=store
    )
    print(type(search_memory_tool))
    print(search_memory_tool)

# --- Section D: Prompt Optimizer Usage ---
async def demo_prompt_optimizer():
    print("\n--- Prompt Optimizer Demo ---\n")
    optimizer = create_prompt_optimizer(MODEL)
    conversation = [
        {"role": "user", "content": "Tell me about the solar system"},
        {"role": "assistant", "content": "The solar system consists of..."},
    ]
    feedback = {"clarity": "needs more structure"}
    trajectories = [(conversation, feedback)]
    better_prompt = await optimizer.ainvoke(
        {"trajectories": trajectories, "prompt": "You are an astronomy expert"}
    )
    print(better_prompt)

    # Prompt memory kind
    optimizer2 = create_prompt_optimizer(MODEL, kind="prompt_memory")
    conversation2 = [
        {"role": "user", "content": "How do I write a bash script?"},
        {"role": "assistant", "content": "Let me explain bash scripting..."},
    ]
    feedback2 = "Response should include a code example"
    trajectories2 = [(conversation2, {"feedback": feedback2})]
    better_prompt2 = await optimizer2(trajectories2, "You are a coding assistant")
    print(better_prompt2)

    # Metaprompt kind
    optimizer3 = create_prompt_optimizer(
        MODEL,
        kind="metaprompt",
        config={"max_reflection_steps": 3, "min_reflection_steps": 1},
    )
    conversation3 = [
        {"role": "user", "content": "Explain quantum computing"},
        {"role": "assistant", "content": "Quantum computing uses..."},
    ]
    feedback3 = "Need better organization and concrete examples"
    trajectories3 = [(conversation3, feedback3)]
    improved_prompt = await optimizer3(
        trajectories3, "You are a quantum computing expert"
    )
    print(improved_prompt)

# --- Section E: Multi-Prompt Optimizer Usage ---
async def demo_multi_prompt_optimizer():
    print("\n--- Multi-Prompt Optimizer Demo ---\n")
    optimizer = create_multi_prompt_optimizer(MODEL)
    conversation = [
        {"role": "user", "content": "Tell me about the solar system"},
        {"role": "assistant", "content": "The solar system consists of..."},
    ]
    feedback = {"clarity": "needs more structure"}
    trajectories = [(conversation, feedback)]
    prompts = [
        {"name": "research", "prompt": "Research the given topic thoroughly"},
        {"name": "summarize", "prompt": "Summarize the research findings"},
    ]
    better_prompts = await optimizer.ainvoke(
        {"trajectories": trajectories, "prompts": prompts}
    )
    print(better_prompts)

    # Prompt memory kind
    optimizer2 = create_multi_prompt_optimizer(MODEL, kind="prompt_memory")
    conversation2 = [
        {"role": "user", "content": "How do I write a bash script?"},
        {"role": "assistant", "content": "Let me explain bash scripting..."},
    ]
    feedback2 = "Response should include a code example"
    trajectories2 = [(conversation2, {"feedback": feedback2})]
    prompts2 = [
        {"name": "explain", "prompt": "Explain the concept"},
        {"name": "example", "prompt": "Provide a practical example"},
    ]
    better_prompts2 = await optimizer2(trajectories2, prompts2)
    print(better_prompts2)

    # Metaprompt kind
    optimizer3 = create_multi_prompt_optimizer(
        MODEL,
        kind="metaprompt",
        config={"max_reflection_steps": 3, "min_reflection_steps": 1},
    )
    conversation3 = [
        {"role": "user", "content": "Explain quantum computing"},
        {"role": "assistant", "content": "Quantum computing uses..."},
    ]
    feedback3 = None
    trajectories3 = [(conversation3, feedback3)]
    prompts3 = [
        {"name": "concept", "prompt": "Explain quantum concepts"},
        {"name": "application", "prompt": "Show practical applications"},
        {"name": "example", "prompt": "Give concrete examples"},
    ]
    improved_prompts = await optimizer3(trajectories3, prompts3)
    print(improved_prompts)

# --- Main entry point ---
async def main():
    await demo_basic_memory_manager()
    await demo_custom_store()
    demo_memory_tool()
    await demo_prompt_optimizer()
    await demo_multi_prompt_optimizer()

if __name__ == "__main__":
    asyncio.run(main())

