import asyncio
import json
import requests
import openai
import os

# Import Agents SDK components.
from agents import (
    Agent,
    Runner,
    function_tool,
    InputGuardrail,
    GuardrailFunctionOutput,
    handoff,
    trace
)

import os
# Set your API keys (replace these with your actual keys).
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
FINANCIAL_MODELING_PREP_API_KEY = "<your_fmp_api_key_here>"
TAVILY_API_KEY = "<your_tavily_api_key_here>"

def get_stock_price(symbol: str) -> dict:
    """
    Fetch the current stock price for the given symbol,
    including volume, 50d & 200d moving averages, EPS, PE, and next earnings announcement.
    """
    url = f"https://financialmodelingprep.com/api/v3/quote-order/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        return {
            "symbol": symbol.upper(),
            "price": data[0]['price'],
            "volume": data[0]['volume'],
            "priceAvg50": data[0]['priceAvg50'],
            "priceAvg200": data[0]['priceAvg200'],
            "EPS": data[0]['eps'],
            "PE": data[0]['pe'],
            "earningsAnnouncement": data[0]['earningsAnnouncement']
        }
    except (IndexError, KeyError):
        return {"error": f"Could not fetch price for symbol: {symbol}"}
    

def get_company_financials(symbol: str) -> dict:
    """
    Fetch basic financial information for the given company symbol.
    Returns industry, sector, company name, market cap, etc.
    """
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        results = data[0]
        return {
            "symbol": results["symbol"],
            "companyName": results["companyName"],
            "marketCap": results["mktCap"],
            "industry": results["industry"],
            "sector": results["sector"],
            "website": results["website"],
            "beta": results["beta"],
            "price": results["price"],
        }
    except (IndexError, KeyError):
        return {"error": f"Could not fetch financials for symbol: {symbol}"}
    

def get_income_statement(symbol: str) -> dict:
    """
    Fetch the latest annual income statement for the given company symbol,
    including revenue, gross profit, net income, EBITDA, EPS, etc.
    """
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        results = data[0]
        return {
            "date": results["date"],
            "revenue": results["revenue"],
            "gross profit": results["grossProfit"],
            "net Income": results["netIncome"],
            "ebitda": results["ebitda"],
            "EPS": results["eps"],
            "EPS diluted": results["epsdiluted"]
        }
    except (IndexError, KeyError):
        return {"error": f"Could not fetch income statement for symbol: {symbol}"}
    

@function_tool
def get_stock_price_tool(symbol: str) -> dict:
    return get_stock_price(symbol)

@function_tool
def get_company_financials_tool(symbol: str) -> dict:
    return get_company_financials(symbol)

@function_tool
def get_income_statement_tool(symbol: str) -> dict:
    return get_income_statement(symbol)


@function_tool
def tavily_search(query: str, include_images: bool = False, search_depth: str = "basic", max_results: int = 1,
                  days: int = 3) -> dict:
    """
    Calls the Tavily Search API to fetch market news based on the query.
    Returns:
        dict: Contains both a formatted summary and the raw JSON response.
    """
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "topic": "general",
        "search_depth": search_depth,
        "max_results": max_results,
        "time_range": None,
        "days": days,
        "include_answer": True,
        "include_raw_content": False,
        "include_images": include_images,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": []
    }
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    # Build a formatted summary.
    summary = ""
    results = result.get("results", [])
    if results:
        for res in results:
            title = res.get("title", "No Title")
            content = res.get("content", "No Content")
            summary += f"Title: {title}\nContent: {content}\n\n"
    else:
        summary = "No text results found.\n"
    if include_images:
        images = result.get("images", [])
        if images:
            summary += "Image Results:\n"
            for image in images:
                summary += f"{image}\n"
        else:
            summary += "No image results found.\n"
    return {
        "formatted_summary": summary,
        "raw_response": result
    }

async def finance_input_guardrail(ctx, agent, input_data: str) -> GuardrailFunctionOutput:
    finance_keywords = ["finance", "investment", "stock", "market", "revenue", "company", "price"]
    is_finance_query = any(keyword in input_data.lower() for keyword in finance_keywords)
    return GuardrailFunctionOutput(output_info={"is_finance_query": is_finance_query},
                                   tripwire_triggered=not is_finance_query)


data_fetch_agent = Agent(
    name="Data Fetch Agent",
    instructions=(
        "You are responsible for fetching financial data. "
        "Based on the query, extract the company symbol and return the stock price, "
        "company financials, and income statement using the provided tools."
    ),
    tools=[get_stock_price_tool, get_company_financials_tool, get_income_statement_tool],
    model="gpt-4o"
)

news_search_agent = Agent(
    name="News Search Agent",
    instructions=(
        "You are a market news search agent. When provided with a finance-related query, "
        "use the tavily_search tool to fetch up-to-date market news."
    ),
    tools=[tavily_search],
    model="gpt-4o"
)

analysis_agent = Agent(
    name="Analysis Agent",
    instructions=(
        "You are a financial analyst. Based on the outputs provided by the Data Fetch Agent and the News Search Agent, "
        "synthesize the following details:\n\n"
        "1. Key financial metrics (e.g., stock price, moving averages, revenue trends).\n"
        "2. Relevant news summaries with titles and key points.\n"
        "3. A clear analysis comparing the current metrics with historical trends and news sentiment.\n\n"
        "Then provide actionable recommendations for retail investors. Be specific and include numbers where applicable."
    ),
    model="gpt-4o"
)

coordinator_agent = Agent(
    name="Financial Coordinator Agent",
    instructions=(
        "You are the central coordinator for financial analysis. First, validate that the query is finance-related. "
        "Then, delegate to the Data Fetch Agent to retrieve financial data and to the News Search Agent to obtain recent market news. "
        "Finally, hand off the combined information to the Analysis Agent to produce a final report."
    ),
    model="gpt-4o",
    handoffs=[data_fetch_agent, news_search_agent, analysis_agent],
    input_guardrails=[InputGuardrail(guardrail_function=finance_input_guardrail)]
)


async def main():
    query = (
        "Provide the latest stock price, company financials, and income statement for AAPL, "
        "and fetch any recent news related to Apple's market performance, "
        "and based on this information, analyze and summarize the key insights and trends for retail investors."
    )

    # Run the coordinator agent which orchestrates all sub-agents.
    with trace(workflow_name="Financial_Data_News_Workflow", group_id="finance_group"):
        result = await Runner.run(coordinator_agent, query)

    # Debug: Print the aggregated conversation history.
    print("Aggregated Conversation History:")
    for message in result.to_input_list():
        print(message)
    print("\n")
    
    # Optionally, run the analysis agent explicitly on the aggregated conversation to force detailed synthesis.
    conversation = result.to_input_list()
    final_result = await Runner.run(analysis_agent, conversation)

    print("Final Financial Analysis Output:")
    print(final_result.final_output)

if __name__ == "__main__":
    asyncio.run(main())