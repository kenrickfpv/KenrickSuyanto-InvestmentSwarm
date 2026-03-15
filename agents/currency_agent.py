import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from tools.get_exchange_rate import get_historical_exchange_rate

currency_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="currency_agent",
    description="An agent that retrieves historical exchange rate data between two currencies over a date range.",
    instruction="""
        You are a foreign exchange data specialist.
        When given two currency codes and a date range, use the get_historical_exchange_rate tool
        to fetch the exchange rate movement.
        Always return the start rate, end rate, and appreciation percentage.
        Common currency codes: MYR, IDR, USD, SGD, EUR, GBP
    """,
    tools=[get_historical_exchange_rate]
)