from agents import Agent, function_tool
from game_master_agent.tools.dice_tool import roll_dice

@function_tool
def roll_tool(sides: int) -> int:
    return roll_dice(sides)

agent = Agent(
    name="NarratorAgent",
    instructions="Narrate the story, call roll_tool for dice-based events.",
    tools=[roll_tool],
)