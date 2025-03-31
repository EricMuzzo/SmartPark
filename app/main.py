from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import httpx
import json
import os

app = FastAPI(
    version="1.1.0",
    summary="Written By Prevail Awoleye",
    contact={
        "name": "Prevail Awoleye"
    }
)

BASE_PRICES = {
    "morning": 0.075,  # 12 AM - 12 PM
    "afternoon": 0.1,  # 12 PM - 6 PM
    "evening": 0.05  # 6 PM - 12 AM
}

MAIN_APP_URL = os.getenv('MAIN_APP_URL')

class PriceRequest(BaseModel):
    timestamp: datetime = Field(..., example="2025-03-08T16:30:00")
    
class PriceResponse(BaseModel):
    minute_rate: float = Field(..., example=0.12)

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

@app.post(
    path="/calculate-rate",
    summary="Returns the pricing rate per minute",
    response_model=PriceResponse,
    status_code=200
)
async def calculate_price(request: PriceRequest):
    base_price = get_base_price(request.timestamp)

    total_spots, occupied_spots = await fetch_spot_data()

    if total_spots == 0:
        raise HTTPException(status_code=400, detail="No parking spots available")
    
    occupancy_rate = occupied_spots / total_spots
    final_price = (1 + occupancy_rate) * base_price

    return PriceResponse(minute_rate=round(final_price, 2))

@app.get("/")
async def root():
    return {"message": "Pricing Service"}