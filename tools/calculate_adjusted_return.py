def calculate_adjusted_return(
    stock_return_percent: float,
    exchange_rate_appreciation_percent: float,
    base_currency: str,
    target_currency: str,
    symbol: str
) -> dict:
    """
    Calculate the real return of a foreign investment after currency adjustment.
    
    Args:
        stock_return_percent: Capital gain % from the stock
        exchange_rate_appreciation_percent: % change in exchange rate (base vs target)
        base_currency: Investor's home currency (e.g., "MYR")
        target_currency: Foreign market currency (e.g., "IDR")
        symbol: Stock symbol (e.g., "BBRI.JK")
    
    Returns:
        Dictionary with real_return and investment recommendation
    """
    try:
        local_return = stock_return_percent / 100
        fx_appreciation = exchange_rate_appreciation_percent / 100

        # Core formula
        real_return = (1 + local_return) / (1 + fx_appreciation) - 1
        real_return_percent = round(real_return * 100, 4)

        # Recommendation logic
        if real_return_percent > 5:
            recommendation = "PROFITABLE — Strong real return after currency adjustment."
        elif real_return_percent > 0:
            recommendation = "MARGINAL — Small positive return. Consider opportunity cost."
        elif real_return_percent > -5:
            recommendation = "RISKY — Slight loss after currency adjustment."
        else:
            recommendation = "NOT RECOMMENDED — Significant loss after currency adjustment."

        return {
            "symbol": symbol,
            "base_currency": base_currency,
            "target_currency": target_currency,
            "stock_return_percent": round(stock_return_percent, 4),
            "fx_appreciation_percent": round(exchange_rate_appreciation_percent, 4),
            "real_return_percent": real_return_percent,
            "recommendation": recommendation
        }

    except Exception as e:
        return {"error": f"Unexpected error: {e}"}