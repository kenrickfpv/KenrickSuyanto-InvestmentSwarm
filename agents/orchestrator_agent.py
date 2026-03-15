import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from agents.stock_agent import stock_agent
from agents.currency_agent import currency_agent
from agents.analysis_agent import analysis_agent

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="orchestrator_agent",
    description="An investment analysis orchestrator that coordinates stock, currency and analysis agents to determine if a foreign investment is profitable after currency adjustment.",
    instruction="""
        You are BMAI — an intelligent investment analysis assistant.
        
        When a user asks whether an investment is profitable, follow these steps:
        
        STEP 1: Use stock_agent to get the stock return percentage
                for the given symbol and date range.
        
        STEP 2: Use currency_agent to get the exchange rate appreciation
                between the investor's home currency and the target currency
                for the same date range.
        
        STEP 3: Use analysis_agent to calculate the real return after
                currency adjustment using the results from Step 1 and Step 2.
        
        STEP 4: Present a clear, friendly summary to the user including:
                - Stock performance
                - Currency movement  
                - Real return after adjustment
                - Final recommendation (PROFITABLE / MARGINAL / RISKY / NOT RECOMMENDED)
        
        Example query: "Will I be profitable investing in BBRI.JK from August 2025 
        while converting MYR to IDR?"
        
        Always ask for clarification if the date range or currencies are not specified.
        For Indonesian stocks use .JK suffix (e.g., BBRI.JK)
        For US stocks use ticker only (e.g., AAPL)
    """,
    tools=[
        AgentTool(stock_agent),
        AgentTool(currency_agent),
        AgentTool(analysis_agent)
    ]
)