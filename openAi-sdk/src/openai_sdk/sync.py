from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import dotenv_values, find_dotenv

def main():
    val = dotenv_values(find_dotenv())

    # Check if the API key is present; if not, raise an error
    if "GEMINI_API_KEY" not in val:
        raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

    # Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=val["GEMINI_API_KEY"],
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )


    agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

    result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

    print("\nCALLING AGENT\n")
    print(result.final_output)

if __name__ == "__main__":
    main()