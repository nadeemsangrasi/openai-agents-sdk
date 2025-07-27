from agents import Runner,enable_verbose_stdout_logging,Agent
from game_master_agent.run_config import config
from game_master_agent.agents.narrator_agent import agent as narrator
from game_master_agent.agents.monster_agent import agent as monster
from game_master_agent.agents.item_agent import agent as item
import asyncio

triage_agent = Agent(
    name="triage_agent",
    instructions="""You are a TriageAgent for the Fantasy Adventure Game Master.
    – If the player’s input concerns combat actions, battle outcomes, or attacking/defending, route it to the MonsterAgent.
    – If they interact with items, treasure, loot, inventory, or random events, route it to the ItemAgent.
    – If they are setting scenes, progressing the storyline, or requesting narration, route it to the NarratorAgent.
    – If the query doesn’t clearly fit combat, items, or narration, answer it yourself.
""",
    handoffs=[narrator,monster,item]
)

async def main():
    is_chat=True
    history=[]
    while is_chat:
        query = input("ME : \t")
        history.append({"role":"user","content":query})
        result = await Runner.run(
            triage_agent,
            f"{query} \nprevious chat : {history}",
            run_config=config
        )
        history.append({"role":"Assistant","content":result.final_output})
        print("AI : ", result.final_output)

def start():
    asyncio.run(main())