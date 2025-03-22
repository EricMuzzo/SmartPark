from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import httpx
import json

app = FastAPI()

BASE_PRICES = {
    "morning": 10,  # 12 AM - 12 PM
    "afternoon": 12,  # 12 PM - 6 PM
    "evening": 8  # 6 PM - 12 AM
}

MAIN_APP_URL = "https://central-api-gud7ethebpctcag5.canadacentral-01.azurewebsites.net"  

class PriceRequest(BaseModel):
    timestamp: datetime = Field(..., example="2025-03-08T16:30:00")

def get_base_price(timestamp: datetime) -> float:

    hour = timestamp.hour
    if 0 <= hour < 12:
        return BASE_PRICES["morning"]
    elif 12 <= hour < 18:
        return BASE_PRICES["afternoon"]
    else:
        return BASE_PRICES["evening"]

async def fetch_spot_data():

    async with httpx.AsyncClient() as client:
        try:
            # Fetch total spots
            total_response = await client.get(f"{MAIN_APP_URL}/spots")
            total_spots_json = json.loads(total_response.content)
            total_spots = total_spots_json['count']
            # Fetch occupied spots
            occupied_response = await client.get(f"{MAIN_APP_URL}/spots?filter=status%3Aeq%3Aoccupied")
            occupied_spots_json = json.loads(occupied_response.content)
            occupied_spots = occupied_spots_json['count']

            return total_spots, occupied_spots
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch spot data: {str(e)}")

@app.post("/calculate-price")
async def calculate_price(request: PriceRequest):
    base_price = get_base_price(request.timestamp)

    total_spots, occupied_spots = await fetch_spot_data()

    if total_spots == 0:
        raise HTTPException(status_code=400, detail="No parking spots available")
    
    occupancy_rate = occupied_spots / total_spots
    final_price = (1 + occupancy_rate) * base_price

    return {"final_price": final_price}