"""The module responsible for connecting and interacting with the pricing microservice.
"""
from datetime import datetime
import random
    
async def fetch_pricing(res_start: datetime, res_end: datetime) -> float:
    """A function to fetch the price from the pricing MS for a given reservation time.

    Args:
        res_start (datetime): Reservation start time
        res_end (datetime): Reservation end time

    Returns:
        float: The price for the reservation
    """
    
    #For now, return a random price
    price = round(random.uniform(0.0, 100.0))
    return price