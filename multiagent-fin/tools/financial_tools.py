import requests
from typing import Dict
from config import ALPHA_VANTAGE_API_KEY, FINANCIAL_MODELING_PREP_API_KEY
from agents import function_tool

import requests
import csv
import io
from typing import Dict, Any

# Base settings for Alpha Vantage
# BASE_URL = "https://www.alphavantage.co/query"
BASE_URL = 'https://financialmodelingprep.com/api/v3'


# print(FINANCIAL_MODELING_PREP_API_KEY)
def get_company_profile(symbol):
    """
    Fetches the company profile including sector, industry, and country.
    Useful for classifying stocks (e.g., Asia Tech).
    """
    print(FINANCIAL_MODELING_PREP_API_KEY)
    # print(f"Running function: get_company_profile with symbol: {symbol}")
    url = f"{BASE_URL}/profile/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    # print(response.json()[0])
    return response.json()[0] if response.ok and response.json() else None


def get_quote(symbol):
    """
    Fetches real-time market data such as latest price, volume, and changes.
    Useful for calculating current exposure in a portfolio.
    """
    print(f"Running function: get_quote with symbol: {symbol}")
    url = f"{BASE_URL}/quote/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    print(f"Fetching quote for {symbol} from {url}")
    response = requests.get(url)
    print(response.json()[0])
    return response.json()[0] if response.ok and response.json() else None


def get_earnings_surprise(symbol):
    """
    Fetches the latest earnings surprise data.
    Includes actual vs estimated EPS to detect beats or misses.
    """
    print(f"Running function: get_earnings_surprise with symbol: {symbol}")
    url = f"{BASE_URL}/earnings-surprises/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    print(response.json()[0:3])
    return response.json()[0] if response.ok and response.json() else None


def get_income_statement_growth(symbol):
    """
    Retrieves annual growth rates for income statement metrics.
    Useful for analyzing revenue and EPS trends over time.
    """
    print(f"Running function: get_income_statement_growth with symbol: {symbol}")
    url = f"{BASE_URL}/income-statement-growth/{symbol}?period=annual&apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    print(response.json()[0])
    return response.json()[0] if response.ok else None


def get_quote_order(symbol):
    """
    Fetches order book quote information (bid/ask prices, size).
    Useful for assessing market liquidity and spread.
    """
    print(f"Running function: get_quote_order with symbol: {symbol}")
    url = f"{BASE_URL}/quote-order/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
    response = requests.get(url)
    print(response.json()[0])
    return response.json() if response.ok else None


@function_tool
def get_company_profile_tool(symbol: str) -> Dict:
    """
    Tool: Returns company profile including sector, industry, and country.
    """
    return get_company_profile(symbol)


@function_tool
def get_quote_tool(symbol: str) -> Dict:
    """
    Tool: Returns real-time market data like price, volume, and change.
    """
    return get_quote(symbol)


@function_tool
def get_earnings_surprise_tool(symbol: str) -> Dict:
    """
    Tool: Returns actual vs. estimated EPS for the latest earnings release.
    """
    return get_earnings_surprise(symbol)

@function_tool
def get_income_statement_growth_tool(symbol: str) -> Dict:
    """
    Tool: Returns annual income statement growth metrics.
    """
    return get_income_statement_growth(symbol)

@function_tool
def get_quote_order_tool(symbol: str) -> Dict:
    """
    Tool: Returns quote order book data (bid/ask levels).
    """
    return get_quote_order(symbol)


# @function_tool
# def get_stock_price_tool(symbol: str) -> Dict:
#     return get_stock_price(symbol)

# @function_tool
# def get_company_financials_tool(symbol: str) -> Dict:
#     return get_company_financials(symbol)

# @function_tool
# def get_income_statement_tool(symbol: str) -> Dict:
#     return get_income_statement(symbol)