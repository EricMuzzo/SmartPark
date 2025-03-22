from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument

from ..utils.auth import get_password_hash
from ..utils.db import users_collection

async def fetch_all_users(filters: dict = {}) -> list:
    """Returns a list of dict user objects from the users collection in database
    Filters have not been documented yet but are functional if you know how to use it.
    """

    users = await users_collection.find(filters).to_list(1000)
    return users


async def fetch_user(id: str) -> dict | None:
    """Returns a dict of a single user object from the users collection in db with mongo id `id`"""
    
    user = await users_collection.find_one({"_id": ObjectId(id)})
    return user


async def create_user(user_data: dict) -> dict:
    """Inserts a user record into the db

    Args:
        user_data (dict): the user object

    Raises:
        HTTPException: When a duplicate key error (username or email) occurs. Ex: trying to 
        create a user with a username or email that another user already has.

    Returns:
        dict: The created user object
    """
    try:
        user_data["password"] = get_password_hash(user_data["password"])
        new_user = await users_collection.insert_one(user_data)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail=f"A user with the provided username or email already exists")
    
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return created_user


async def update_user(id: str, data: dict) -> dict | JSONResponse:
    """Updates a document in the user collection in db with matching mongo id `id` and
    returns the updated user. If no update parameters were passed, the current user document
    is returned.

    Args:
        id (str): Mongo object id
        data (dict): fields to update

    Returns:
        dict | JSONResponse: Returns the updated user dict or a JSONResponse when a DuplicateKeyError arises
    """
    if "password" in data:
        data["password"] = get_password_hash(data["password"])
    
    if len(data) >= 1:
        
        try:
            update_result = await users_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": data},
                return_document=ReturnDocument.AFTER
            )
        except DuplicateKeyError:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Duplicate key error",
                    "message": "Record with given unique username or email already exists"
                }
            )
            
        return update_result
    
    #Update is empty, but still return the matching document
    existing_user = await users_collection.find_one({"_id": ObjectId(id)})
    return existing_user


async def remove_user(id: str) -> bool:
    """Deletes a user with the mongo id `id` from the users collection.

    Args:
        id (str): Mongo object id

    Returns:
        bool: `True` if the delete was successful. `False` otherwise.
    """
    result = await users_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return True
    return False