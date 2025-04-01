from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing import Optional, Annotated, List, Literal
from bson import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]

class ParkingSpotBase(BaseModel):
    floor_level: int = Field(..., example=3)
    spot_number: int = Field(..., example=57)
    status: Literal['vacant', 'occupied', 'reserved'] = Field(default='vacant', description="State of the spot. Can only be vacant, occupied, or reserved")
    
class ParkingSpot(ParkingSpotBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        
        
class ParkingSpotUpdate(BaseModel):
    status: Literal['vacant', 'occupied', 'reserved'] = Field(None, description="State of the spot. Can only be vacant, occupied, or reserved")
    
    
class ParkingSpotCollection(BaseModel):
    spots: List[ParkingSpot]
    
