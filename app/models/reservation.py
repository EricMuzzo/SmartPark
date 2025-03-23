from pydantic import BaseModel, Field, FutureDatetime
from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated, List
from bson import ObjectId
from datetime import datetime
        
PyObjectId = Annotated[str, BeforeValidator(str)]        


class ReservationBase(BaseModel):
    """The pydantic base model of a reservation"""
    user_id: PyObjectId = Field(..., description="The mongo ObjectID of the user who made the reservation", example="67db7a51a8b9b8789e7090a0")
    spot_id: PyObjectId = Field(..., description="The mongo ObjectID of reserved parking spot", example="67ccb76f825b86fb6abcae71")
    start_time: datetime = Field(..., description="The start time of the reservation", example=datetime(2025, 3, 29, 18, 0, 0))
    end_time: datetime = Field(..., description="The end time of the reservation", example=datetime(2025, 3, 29, 18, 30, 0))
    

class ReservationCreate(BaseModel):
    """The pydantic base model for creating a reservation"""
    user_id: PyObjectId = Field(..., description="The mongo ObjectID of the user who made the reservation", example="67db7a51a8b9b8789e7090a0")
    spot_id: PyObjectId = Field(..., description="The mongo ObjectID of reserved parking spot", example="67ccb76f825b86fb6abcae71")
    start_time: FutureDatetime = Field(..., description="The start time of the reservation", example=datetime(2025, 3, 29, 18, 0, 0))
    end_time: FutureDatetime = Field(..., description="The end time of the reservation", example=datetime(2025, 3, 29, 18, 30, 0))
    
    
class Reservation(ReservationBase):
    """DB representation of a reservation"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    final_price: float = Field(..., description="The total paid price of the reservation")
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
    
    
class ReservationCollection(BaseModel):
    """Stores a list of `Reservation` objects"""
    reservations: List[Reservation]