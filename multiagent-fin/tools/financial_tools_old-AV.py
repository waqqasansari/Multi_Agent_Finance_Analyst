import requests
from typing import Dict
from config import ALPHA_VANTAGE_API_KEY, FINANCIAL_MODELING_PREP_API_KEY
from agents import function_tool

import requests
import csv
import io
from typing import Dict, Any

# Base settings for Alpha Vantage
BASE_URL = "https://www.alphavantage.co/query"

# def get_stock_price(symbol: str) -> Dict:
#     """Fetch current stock price and key metrics"""
#     url = f"https://financialmodelingprep.com/api/v3/quote-order/{symbol}?apikey={FINANCIAL_MODELING_PREP_API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     try:
#         return {
#             "symbol": symbol.upper(),
#             "price": data[0]['price'],
#             "volume": data[0]['volume'],
#             "priceAvg50": data[0]['priceAvg50'],
#             "priceAvg200": data[0]['priceAvg200'],
#             "EPS": data[0]['eps'],
#             "PE": data[0]['pe'],
#             "earningsAnnouncement": data[0]['earningsAnnouncement']
#         }
#     except (IndexError, KeyError):
#         return {"error": f"Could not fetch price for symbol: {symbol}"}

def get_stock_price(symbol: str) -> Dict[str, Any]:
    """
    Fetch the current stock price for the given symbol,
    including volume, 50d & 200d moving averages, EPS, P/E,
    and the next earnings announcement date.
    """
    print(f"Running function: get_stock_price with symbol: {symbol}")
    try:
        # 1. GLOBAL_QUOTE for price & volume
        params_quote = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        resp = requests.get(BASE_URL, params=params_quote)
        resp.raise_for_status()
        quote = resp.json().get("Global Quote", {})

        price = float(quote.get("05. price", 0))
        volume = int(quote.get("06. volume", 0))

        # 2. OVERVIEW for moving averages, EPS, and P/E ratio
        params_ov = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        resp = requests.get(BASE_URL, params=params_ov)
        resp.raise_for_status()
        ov = resp.json()

        price_avg_50 = float(ov.get("50DayMovingAverage", 0))
        price_avg_200 = float(ov.get("200DayMovingAverage", 0))
        eps = float(ov.get("EPS", 0))
        pe = float(ov.get("PERatio", 0))

        # 3. EARNINGS_CALENDAR for next earnings date (CSV)
        params_ec = {
            "function": "EARNINGS_CALENDAR",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        resp = requests.get(BASE_URL, params=params_ec)
        resp.raise_for_status()
        f = io.StringIO(resp.text)
        reader = csv.DictReader(f)
        next_earn = next(reader, {})
        earnings_date = next_earn.get("reportDate")
        print({
            "symbol": symbol.upper(),
            "price": price,
            "volume": volume,
            "priceAvg50": price_avg_50,
            "priceAvg200": price_avg_200,
            "EPS": eps,
            "PE": pe,
            "earningsAnnouncement": earnings_date
        })

        return {
            "symbol": symbol.upper(),
            "price": price,
            "volume": volume,
            "priceAvg50": price_avg_50,
            "priceAvg200": price_avg_200,
            "EPS": eps,
            "PE": pe,
            "earningsAnnouncement": earnings_date
        }
    except (requests.RequestException, ValueError, KeyError) as e:
        return {"error": f"Could not fetch price for symbol: {symbol}. Error: {e}"}

def get_company_financials(symbol: str) -> Dict[str, Any]:
    """
    Fetch basic financial information for the given company symbol,
    including industry, sector, company name, market cap, beta, and current price.
    """
    print(f"Running function: get_company_financials with symbol: {symbol}")
    try:
        # 1. OVERVIEW for company fundamentals
        params_ov = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        resp = requests.get(BASE_URL, params=params_ov)
        resp.raise_for_status()
        ov = resp.json()

        # 2. GLOBAL_QUOTE for current price
        price_data = get_stock_price(symbol)
        price = price_data.get("price")

        return {
            "symbol": ov.get("Symbol"),
            "companyName": ov.get("Name"),
            "marketCap": ov.get("MarketCapitalization"),
            "industry": ov.get("Industry"),
            "sector": ov.get("Sector"),
            "website": None,  # not provided by Alpha Vantage
            "beta": ov.get("Beta"),
            "price": price
        }
    except (requests.RequestException, KeyError) as e:
        return {"error": f"Could not fetch financials for symbol: {symbol}. Error: {e}"}


def get_income_statement(symbol: str) -> Dict[str, Any]:
    """
    Fetch the latest annual income statement for the given company symbol,
    including revenue, gross profit, net income, EBITDA, EPS, and diluted EPS.
    """
    print(f"Running function: get_income_statement with symbol: {symbol}")
    try:
        # 1. INCOME_STATEMENT for annual reports
        params_is = {
            "function": "INCOME_STATEMENT",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        resp = requests.get(BASE_URL, params=params_is)
        resp.raise_for_status()
        data = resp.json().get("annualReports", [])
        if not data:
            return {"error": f"No income statement found for symbol: {symbol}"}
        inc = data[0]  # latest

        # 2. OVERVIEW for EPS & Diluted EPS
        params_ov = {
            "function": "OVERVIEW",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        resp = requests.get(BASE_URL, params=params_ov)
        resp.raise_for_status()
        ov = resp.json()

        return {
            "date": inc.get("fiscalDateEnding"),
            "revenue": inc.get("totalRevenue"),
            "gross profit": inc.get("grossProfit"),
            "net Income": inc.get("netIncome"),
            "ebitda": inc.get("ebitda"),
            "EPS": ov.get("EPS"),
            "EPS diluted": ov.get("DilutedEPSTTM")
        }
    except (requests.RequestException, KeyError) as e:
        return {"error": f"Could not fetch income statement for symbol: {symbol}. Error: {e}"}
    
@function_tool
def get_stock_price_tool(symbol: str) -> Dict:
    return get_stock_price(symbol)

@function_tool
def get_company_financials_tool(symbol: str) -> Dict:
    return get_company_financials(symbol)

@function_tool
def get_income_statement_tool(symbol: str) -> Dict:
    return get_income_statement(symbol)