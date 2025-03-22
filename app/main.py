from fastapi import FastAPI
from .routers import users, authentication, reservations, spots
from .utils.db import create_indexes, close_mongo_connection

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
    version="1.0.3"
)

@app.on_event("startup")
async def startup_db_client():
    await create_indexes()
    
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

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