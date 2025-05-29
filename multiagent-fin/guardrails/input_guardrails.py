# from agents import GuardrailFunctionOutput

# async def finance_input_guardrail(ctx, agent, input_data: str) -> GuardrailFunctionOutput:
#     finance_keywords = ["finance", "investment", "stock", "market", "revenue", "company", "price"]
#     is_finance_query = any(keyword in input_data.lower() for keyword in finance_keywords)
#     return GuardrailFunctionOutput(
#         output_info={"is_finance_query": is_finance_query},
#         tripwire_triggered=not is_finance_query
#     )


from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel

# Step 1: Define the structured output
class FinanceOutput(BaseModel):
    is_finance_query: bool
    reasoning: str

# Step 2: Create the guardrail agent
guardrail_agent = Agent(
    name="Finance Guardrail Checker",
    instructions=(
        "Determine whether the user's query is related to finance topics like investment, "
        "stock market, revenue, or company prices. Respond with `is_finance_query = true` if so. "
        "Also provide reasoning for your decision."
    ),
    model="gpt-4.1-mini-2025-04-14",
    output_type=FinanceOutput,
)

# Step 3: Implement the guardrail function
async def finance_input_guardrail(ctx, agent, input_data: str) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(FinanceOutput)
    
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_finance_query,
    )