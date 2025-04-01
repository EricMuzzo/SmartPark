"""The module responsible for connecting and interacting with the pricing microservice."""

from datetime import datetime
import math
import os
import httpx

PRICING_URL = os.getenv("PRICING_URL")
    
async def fetch_pricing(res_start: datetime, res_end: datetime) -> float:
    """A function to fetch the price from the pricing MS for a given reservation time.
    This function fetches the rate/minute and computes the total price.

    Args:
        res_start (datetime): Reservation start time
        res_end (datetime): Reservation end time

    Returns:
        float: The price for the reservation
    """
    payload = {
        "timestamp": datetime.isoformat(res_start)
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PRICING_URL}/calculate-rate", follow_redirects=True, json=payload)
    response.raise_for_status()
    
    minute_rate: float = response.json()["minute_rate"]

    #Calculate total reservation time, rounded up to nearest minute
    time_diff = res_end - res_start
    total_minutes = math.ceil(time_diff.total_seconds() / 60)

    total_price = round((total_minutes * minute_rate), 2)
    
    return total_price