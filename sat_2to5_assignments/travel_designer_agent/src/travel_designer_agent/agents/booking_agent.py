from agents import Agent, function_tool
from travel_designer_agent.tools.hotels_tool import suggest_hotels
from travel_designer_agent.tools.flights_tool import get_flights
@function_tool
def hotels_tool(city: str) -> list:
    return suggest_hotels(city)

@function_tool
def flights_tool(origin: str, dest: str) -> list:
    return get_flights(origin, dest)

agent = Agent(
    name="BookingAgent",
    instructions="suggest hotels in the destination city using hotels_tool and flights using flights_tool.",
    tools=[hotels_tool,flights_tool],
)