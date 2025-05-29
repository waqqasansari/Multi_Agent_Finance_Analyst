from agents import Agent, InputGuardrail
# from tools.financial_tools import (
#     get_stock_price_tool,
#     get_company_financials_tool,
#     get_income_statement_tool
# )

from tools.financial_tools import (
    get_company_profile_tool,
    get_quote_tool,
    get_earnings_surprise_tool,
    get_income_statement_growth_tool,
    get_quote_order_tool
)

from tools.search_tools import tavily_search
from guardrails.input_guardrails import finance_input_guardrail
import os
# API Configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

def create_agents():
    print("⚠️ AGENTS BEING INITIALIZED (THIS SHOULD HAPPEN ONCE)")
    # data_fetch_agent = Agent(
    #     name="Data Fetch Agent",
    #     instructions="Fetch financial data using provided tools, for the multiple companies specified in the query then return the results for the multiple companies.",
    #     tools=[get_stock_price_tool, get_company_financials_tool, get_income_statement_tool],
    #     model="gpt-4.1-mini-2025-04-14"
    # )

    data_fetch_agent = Agent(
    name="Data Fetch Agent",
    instructions=(
        "Use the available tools to fetch detailed financial data for the companies specified in the query. "
        "This includes stock prices, company profiles, earnings surprises, real-time quotes, financials, income statement growth, "
        "and order book data. Aggregate and return the results clearly for each company."
        "Ensure to handle multiple companies in the query and provide structured output."
        "Also for a query you do not need to use all the tools, you can use only the required tools based on the query."),
    tools=[
        get_company_profile_tool,
        get_quote_tool,
        get_earnings_surprise_tool,
        get_income_statement_growth_tool,
        get_quote_order_tool
    ],
    model="gpt-4.1-mini-2025-04-14"
)

    news_search_agent = Agent(
        name="News Search Agent",
        instructions="Fetch market news using Tavily",
        tools=[tavily_search],
        model="gpt-4.1-mini-2025-04-14"
    )

    analysis_agent = Agent(
        name="Analysis Agent",
        instructions="Analyze financial data and news, and return the analysis in a structured format.",
        model="gpt-4.1-mini-2025-04-14"
    )

    start_language_agent = Agent(
        name="Financial Coordinator Agent",
        instructions="Coordinate financial analysis workflow, generate the output in the speech format, and ensure all agents are utilized effectively. you can use the search agent to fetch market news, the data fetch agent to get financial data, and the analysis agent to analyze the data and news. Return the final analysis in a structured format. and there might be a case where the user query is required only news search, in that case, you can use the news search agent to fetch market news and return the results.",
        model="gpt-4.1-mini-2025-04-14",
        handoffs=[data_fetch_agent, news_search_agent, analysis_agent],
        input_guardrails=[InputGuardrail(guardrail_function=finance_input_guardrail)]
    )
    
    return {
        "data_fetch": data_fetch_agent,
        "news_search": news_search_agent,
        "analysis": analysis_agent,
        "start_language_agent": start_language_agent
    }