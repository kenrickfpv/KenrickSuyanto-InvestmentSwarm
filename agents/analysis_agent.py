import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from tools.calculate_adjusted_return import calculate_adjusted_return

analysis_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="analysis_agent",
    description="An agent that calculates the real return of a foreign investment after adjusting for currency fluctuation.",
    instruction="""
        You are an investment analysis specialist.
        When given stock return percentage, exchange rate appreciation percentage,
        currency codes and stock symbol, use the calculate_adjusted_return tool
        to compute the real return after currency adjustment.
        Always provide a clear recommendation based on the result.
        The formula used is: (1 + stock_return) / (1 + fx_appreciation) - 1
    """,
    tools=[calculate_adjusted_return]
    
)