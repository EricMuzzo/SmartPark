from fastapi import HTTPException
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument

from ..utils.db import spots_collection


async def fetch_all_spots(filters: dict = {}) -> list:
    """Returns a list of dict `ParkingSpot` objects from the parking spots collection in database
    """

    spots = await spots_collection.find(filters).to_list(1000)
    return spots


async def fetch_spot(id: str) -> dict | None:
    """Returns a dict of a single `ParkingSpot` object from the parking spots
    collection in db with mongo id `id`"""
    
    spots = await spots_collection.find_one({"_id": ObjectId(id)})
    return spots


async def create_spot(spot_data: dict) -> dict:
    """Inserts a spot record into the db.

    Args:
        spot_data (dict): the spot dict object

    Raises:
        HTTPException: When the provided combination of floor_level and spot_number already exists

    Returns:
        dict: the dict of the inserted spot record
    """
    try:
        new_spot = await spots_collection.insert_one(spot_data)
    except DuplicateKeyError:
        raise HTTPException(400, detail="A spot with the provided combination of floor_level and spot_number already exists")
    
    created_spot = await spots_collection.find_one({"_id": new_spot.inserted_id})
    return created_spot


async def update_spot(id: str, data: dict) -> dict:
    """Updates a document in the parking spots collection in db with matching mongo id `id` and
    returns the updated spot. If no update parameters were passed, the current spot document
    is returned.

    Args:
        id (str): Mongo object id
        data (dict): The fields to update

    Raises:
        HTTPException: When the provided combination of floor_level and spot_number already exists

    Returns:
        dict: Returns the updated spot dict
    """
    if len(data) >= 1:
        
        try:
            update_result = await spots_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": data},
                return_document=ReturnDocument.AFTER
            )
        except DuplicateKeyError:
            raise HTTPException(400, detail="A spot with the provided combination of floor_level and spot_number already exists")
            
        return update_result
    
    #Update is empty, but still return the matching document
    existing_spot = await spots_collection.find_one({"_id": ObjectId(id)})
    return existing_spot


async def remove_spot(id: str) -> bool:
    """Deletes a spot with the mongo id `id` from the spots collection.

    Args:
        id (str): Mongo object id

    Returns:
        bool: `True` if the delete was successful. `False` otherwise.
    """
    result = await spots_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return True
    return False