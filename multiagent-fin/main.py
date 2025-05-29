import asyncio
from agents import Runner, trace
from agents_.agent_definitions import create_agents

from agents import (
    InputGuardrailTripwireTriggered,
    Runner
)

import os
# API Configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

async def main():
    agent_dict = create_agents()
    # print(agent_dict)
    # query = (
    #     "Provide the latest financial data and analysis for AAPL, "
    #     "including recent market news and investor recommendations."
    # )
    query = ("Analyze the recent earnings surprises of TSMC and Samsung, and assess their impact on the Asia tech sector.")

    with trace(workflow_name="Financial_Analysis", group_id="finance_1"):
        try:
            result = await Runner.run(agent_dict["start_language_agent"], query, previous_response_id=result.last_response_id if 'result' in locals() else None)
            print(result)
            print("Analysis Results:")
            print(result.final_output)
        except InputGuardrailTripwireTriggered as e:
            print(f"Guardrail triggered: {e}")

if __name__ == "__main__":
    asyncio.run(main())