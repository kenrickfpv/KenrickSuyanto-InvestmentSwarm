import httpx
from datetime import datetime, timedelta

def get_historical_exchange_rate(
    base_currency: str,
    target_currency: str,
    start_date: str,
    end_date: str
) -> dict:
    """
    Get exchange rate between two currencies over a date range.
    
    Args:
        base_currency: The currency to convert from (e.g., "MYR")
        target_currency: The currency to convert to (e.g., "IDR")
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary with start_rate, end_rate and appreciation_percent
    """
    try:
        url = f"https://api.frankfurter.app/{start_date}..{end_date}"
        params = {"from": base_currency, "to": target_currency}
        
        response = httpx.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        rates = data["rates"]
        dates = sorted(rates.keys())
        
        start_rate = rates[dates[0]][target_currency]
        end_rate = rates[dates[-1]][target_currency]
        
        appreciation_percent = ((end_rate - start_rate) / start_rate) * 100
        
        return {
            "base_currency": base_currency,
            "target_currency": target_currency,
            "start_date": dates[0],
            "end_date": dates[-1],
            "start_rate": round(start_rate, 4),
            "end_rate": round(end_rate, 4),
            "appreciation_percent": round(appreciation_percent, 4)
        }
    
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}