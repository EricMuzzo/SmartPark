import os
import motor.motor_asyncio

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client.get_database(DB_NAME)

reservations_collection = database.get_collection("reservations")
users_collection = database.get_collection("users")
spots_collection = database.get_collection("parking_spots")

async def create_indexes():
    await users_collection.create_index("username", unique=True, name="uname_unique")
    await users_collection.create_index("email", unique=True, name="email_unique")
    await spots_collection.create_index([("floor_level", 1), ("spot_number", 1)], unique=True)
    print("Connected to database")

async def close_mongo_connection() -> None:
    client.close()
    print("Disconnected from MongoDB database")