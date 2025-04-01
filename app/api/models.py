from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal

# Generic Models
@dataclass
class ListResponse:
    records: List[object]
    count: int = 0  # Will be computed in API client

@dataclass
class Token:
    access_token: str
    token_type: str

@dataclass
class TokenData:
    username: Optional[str] = None

# User Models
@dataclass
class UserBase:
    username: str
    name: str
    email: str

@dataclass
class User(UserBase):
    _id: Optional[str]

@dataclass
class UserCreate(UserBase):
    password: str

@dataclass
class UserUpdate:
    username: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

@dataclass
class UserCollection:
    users: List[User]

@dataclass
class UserSignUp(User):
    token: Token

@dataclass
class UserFilterParams:
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None

# Spot Models
@dataclass
class ParkingSpotBase:
    floor_level: int
    spot_number: int
    status: Literal["vacant", "occupied", "reserved"] = "vacant"

@dataclass
class ParkingSpot(ParkingSpotBase):
    _id: Optional[str] = None

@dataclass
class ParkingSpotUpdate:
    status: Optional[Literal["vacant", "occupied", "reserved"]] = None

@dataclass
class ParkingSpotCollection:
    spots: List[ParkingSpot]

# Reservation Models
@dataclass
class ReservationBase:
    user_id: str
    spot_id: str
    start_time: datetime
    end_time: datetime

@dataclass
class ReservationCreate:
    user_id: str
    spot_id: str
    start_time: str
    end_time: str

@dataclass
class Reservation(ReservationBase):
    _id: Optional[str]
    final_price: float

@dataclass
class ReservationCollection:
    reservations: List[Reservation]