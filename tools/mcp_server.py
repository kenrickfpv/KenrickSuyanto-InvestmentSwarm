import asyncio
import logging
import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from get_stock_return import get_stock_return
from get_exchange_rate import get_historical_exchange_rate
from calculate_adjusted_return import calculate_adjusted_return

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("JarvisAI Investment MCP Server 📈")


@mcp.tool()
def fetch_stock_return(symbol: str, start_date: str, end_date: str) -> dict:
    """
    Fetch stock capital gain percentage between two dates.
    
    Args:
        symbol: Stock ticker (e.g., BBRI.JK for Indonesian, AAPL for US)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary with start_price, end_price, return_percent
    """
    logger.info(f"--- 🛠️ Tool: fetch_stock_return called for {symbol} ---")
    return get_stock_return(symbol, start_date, end_date)


@mcp.tool()
def fetch_exchange_rate(
    base_currency: str,
    target_currency: str,
    start_date: str,
    end_date: str
) -> dict:
    """
    Fetch historical exchange rate between two currencies.
    
    Args:
        base_currency: Investor home currency (e.g., MYR)
        target_currency: Foreign market currency (e.g., IDR)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary with start_rate, end_rate, appreciation_percent
    """
    logger.info(f"--- 🛠️ Tool: fetch_exchange_rate called for {base_currency}/{target_currency} ---")
    return get_historical_exchange_rate(base_currency, target_currency, start_date, end_date)


@mcp.tool()
def compute_adjusted_return(
    stock_return_percent: float,
    exchange_rate_appreciation_percent: float,
    base_currency: str,
    target_currency: str,
    symbol: str
) -> dict:
    """
    Calculate real investment return after currency adjustment.
    Formula: (1 + stock_return) / (1 + fx_appreciation) - 1
    
    Args:
        stock_return_percent: Capital gain % from stock
        exchange_rate_appreciation_percent: % change in exchange rate
        base_currency: Investor home currency (e.g., MYR)
        target_currency: Foreign market currency (e.g., IDR)
        symbol: Stock symbol
    
    Returns:
        Dictionary with real_return_percent and recommendation
    """
    logger.info(f"--- 🛠️ Tool: compute_adjusted_return called for {symbol} ---")
    return calculate_adjusted_return(
        stock_return_percent,
        exchange_rate_appreciation_percent,
        base_currency,
        target_currency,
        symbol
    )


if __name__ == "__main__":
    logger.info(f"🚀 JarvisAI MCP Server started on port {os.getenv('PORT', 8080)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8080)),
        )
    )