from agents import Runner,enable_verbose_stdout_logging,Agent
from travel_designer_agent.run_config import config
from travel_designer_agent.agents.destination_agent import agent as DestinationAgent
from travel_designer_agent.agents.booking_agent import agent as BookingAgent
from travel_designer_agent.agents.explore_agent import agent as ExploreAgent
import asyncio

triage_agent = Agent(
    name="triage_agent",
    instructions="""You are a TriageAgent for the AI Travel Designer application.
– If the user’s request involves finding or booking flights, forward it to the DestinationAgent.
– If they inquire about hotel reservations or lodging, forward it to the BookingAgent.
– If they want local attractions, sightseeing tips, or things to do, forward it to the ExploreAgent.
– If the query doesn’t clearly match flights, hotels, or attractions, answer it yourself.""",
    handoffs=[DestinationAgent,BookingAgent,ExploreAgent]
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