from agents import Agent, function_tool
from game_master_agent.tools.event_tool import generate_event

@function_tool
def event_tool() -> str:
    return generate_event()

agent = Agent(
    name="ItemAgent",
    instructions="Manage inventory events and rewards using event_tool.",
    tools=[event_tool],
)