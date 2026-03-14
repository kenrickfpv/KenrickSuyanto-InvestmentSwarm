import yfinance as yf
from datetime import datetime, timedelta

def get_stock_return(symbol: str, start_date: str, end_date: str) -> dict:
    """
    Get the capital gain percentage of a stock between two dates.
    
    Args:
        symbol: Stock ticker symbol (e.g., "BUMI.JK" for PT Bumi, "AAPL" for Apple)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary containing start_price, end_price, and return_percent
    """
    try:
        # Add one day to end_date to make it inclusive
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        end_date_inclusive = end_dt.strftime("%Y-%m-%d")
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date_inclusive)
        
        if df.empty:
            return {"error": f"No data found for symbol {symbol}"}
        
        start_price = float(df.iloc[0]["Close"])
        end_price = float(df.iloc[-1]["Close"])
        actual_start = df.index[0].strftime("%Y-%m-%d")
        actual_end = df.index[-1].strftime("%Y-%m-%d")
        
        return_percent = ((end_price - start_price) / start_price) * 100
        
        return {
            "symbol": symbol,
            "start_date": actual_start,
            "end_date": actual_end,
            "start_price": round(start_price, 4),
            "end_price": round(end_price, 4),
            "return_percent": round(return_percent, 4)
        }
    
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}