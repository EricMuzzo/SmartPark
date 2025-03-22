from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated, List
from bson import ObjectId
from datetime import datetime
        
PyObjectId = Annotated[str, BeforeValidator(str)]        

class ReservationBase(BaseModel):
    """The pydantic base model of a reservation. Doubles as the model for res creation"""
    user_id: PyObjectId = Field(..., description="The mongo ObjectID of the user who made the reservation")
    spot_id: PyObjectId = Field(..., description="The mongo ObjectID of reserved parking spot")
    start_time: datetime = Field(..., description="The UTC start time of the reservation", example="2025-03-08T16:30:00")
    end_time: datetime = Field(..., description="The UTC end time of the reservation", example="2025-03-08T16:30:00")
    
    
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