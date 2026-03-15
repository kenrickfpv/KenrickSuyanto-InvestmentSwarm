import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from tools.get_stock_return import get_stock_return

stock_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="stock_agent",
    description="An agent that retrieves stock price data and calculates capital gain percentage for a given stock symbol and date range.",
    instruction="""
        You are a stock market data specialist.
        When given a stock symbol and date range, use the get_stock_return tool
        to fetch the stock's performance data.
        Always return the start price, end price, and return percentage.
        For Indonesian stocks, the symbol format is TICKER.JK (e.g., BBRI.JK, BUMI.JK)
        For US stocks, just use the ticker (e.g., AAPL, GOOGL)
    """,
    tools=[get_stock_return]
)