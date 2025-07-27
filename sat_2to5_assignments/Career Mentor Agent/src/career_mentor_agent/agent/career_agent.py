from agents import Agent, function_tool
from career_mentor_agent.tools.career_tool import get_career_roadmap

@function_tool
def career_roadmap_tool(field: str):
    return get_career_roadmap(field)

agent = Agent(
    name="CareerAgent",
    instructions="You suggest three career fields based on a student’s interests and available skills.",
    tools=[career_roadmap_tool],
)