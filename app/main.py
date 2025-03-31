# import dotenv
# dotenv.load_dotenv()

from fastapi import FastAPI
from .utils.db import create_indexes, close_mongo_connection
from .utils.rabbit_connector import init_rabbit, teardown_rabbit
from .routers import users, authentication, reservations, spots

#============================================================
#   Metadata/Constants
#============================================================

description = """
A centralized RESTful API for the Smart Parking System application
"""


#============================================================
#   Application setup
#============================================================

app = FastAPI(
    title="Central API",
    description=description,
    version="1.2.0",
    contact={
        "name": "Eric Muzzo",
        "email": "ericm02@me.com"
    }
)

@app.on_event("startup")
async def startup_db_client():
    await create_indexes()
    init_rabbit()
    
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    teardown_rabbit()

#============================================================
#   Register the routes
#============================================================

app.include_router(users.router)
app.include_router(spots.router)
app.include_router(reservations.router)
app.include_router(authentication.router)


@app.get("/")
async def root():
    return {"message": "FastAPI Central Server"}