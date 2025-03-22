from fastapi import HTTPException
from bson import ObjectId

from ..utils.db import reservations_collection
from ..utils.pricing_connector import fetch_pricing
from ..models.reservation import Reservation


#=============================================================
#   Utility functions used in main CRUD operations
#=============================================================

async def find_conflict(reservation_data: dict) -> dict | None:
    """Checks the reservations collection for an existing reservation that has a time
    conflict with the reservation trying to be created for a matching `spot_id`

    Args:
        reservation_data (dict): The reservation object data

    Returns:
        dict | None: The conflicting document from the reservations collection if one exists.
        Otherwise returns `None`
    """
    conflict = await reservations_collection.find_one({
        "spot_id": ObjectId(reservation_data["spot_id"]),
        "start_time": {"$lt": reservation_data["end_time"]},
        "end_time":   {"$gt": reservation_data["start_time"]}
    })
    
    return conflict


#=============================================================
#   Main CRUD operations
#=============================================================

async def fetch_all_reservations(filters: dict = {}) -> list:
    """Returns a list of dict reservation objects from the reservations collection in database
    """

    reservations = await reservations_collection.find(filters).to_list(1000)
    return reservations


async def fetch_reservation(id: str) -> dict | None:
    """Returns a dict of a single reservation object from the reservations
    collection in db with mongo id `id`"""
    
    reservation = await reservations_collection.find_one({"_id": ObjectId(id)})
    return reservation


async def create_reservation(reservation_data: dict) -> dict:
    """Inserts a reservation record into the db. This function checks to see whether
    a conflict will occur between an existing reservation and the one trying to be created.

    Args:
        reservation_data (dict): the reservation object

    Raises:
        HTTPException: When a duplicate key error (username or email) occurs. Ex: trying to 
        create a user with a username or email that another user already has.

    Returns:
        dict: The created user object
    """
    
    #First check if a reservation conflict exists
    conflict = await find_conflict(reservation_data)
    if conflict is not None:
        raise HTTPException(status_code=400, detail="Conflict with existing reservation")
    
    #Now we need to fetch pricing from the pricing microservice. This should not be sent as part of the request
    #since that opens the possibility of someone tampering with the req body and inserting their own price.
    #For now, I will simulate this until the ms is ready.
    price = await fetch_pricing(reservation_data["start_time"], reservation_data["end_time"])
    
    #build a reservation object
    reservation = Reservation(
        user_id = reservation_data["user_id"],
        spot_id = reservation_data["spot_id"],
        start_time = reservation_data["start_time"],
        end_time = reservation_data["end_time"],
        final_price = price
    )
    
    payload = reservation.model_dump(by_alias=True, exclude=["id"])
    
    #Now change back the id strings to ObjectId fields
    payload["user_id"] = ObjectId(payload["user_id"])
    payload["spot_id"] = ObjectId(payload["spot_id"])
    
    new_reservation = await reservations_collection.insert_one(payload)
    created_reservation = await reservations_collection.find_one({"_id": new_reservation.inserted_id})
    return created_reservation



async def remove_reservation(id: str) -> bool:
    """Deletes a reservation with the mongo id `id` from the reservation collection.

    Args:
        id (str): Mongo object id

    Returns:
        bool: `True` if the delete was successful. `False` otherwise.
    """
    result = await reservations_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return True
    return False