from agents import Agent, function_tool
from career_mentor_agent.tools.skill_tool import get_skill_plan

@function_tool
def skill_plan_tool(skill: str):
    return get_skill_plan(skill)

agent = Agent(
    name="SkillAgent",
    instructions="Given a chosen skill, generate a structured 3-step learning plan.",
    tools=[skill_plan_tool],
)