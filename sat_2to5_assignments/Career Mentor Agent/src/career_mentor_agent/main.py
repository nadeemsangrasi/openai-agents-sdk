from agents import Runner,Agent,enable_verbose_stdout_logging
from career_mentor_agent.run_config import config
from career_mentor_agent.agent.career_agent import agent as career_agent
from career_mentor_agent.agent.skill_agent import agent as skill_agent
from career_mentor_agent.agent.job_agent import agent as job_agent
import asyncio

triage_agent = Agent(
    name="triage_agent",
    instructions="""You are a TriageAgent for the Career Mentor application.
– When the user’s query is about job openings, resumes, interview tips, or hiring processes, forward it to the JobAgent.
– When they seek long‑term career guidance, choosing a field, or planning their professional path, forward it to the CareerAgent.
– When they ask how to learn or improve a particular skill, training plan, or practice exercise, forward it to the SkillAgent.
– If the query doesn’t clearly match any of the above categories, answer it yourself.""",
    handoffs=[career_agent,skill_agent,job_agent]
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