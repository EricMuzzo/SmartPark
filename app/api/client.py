import requests
from datetime import datetime
from config import config
from api.models import (
    User, UserCreate, UserUpdate, UserSignUp, Token, ListResponse,
    ParkingSpot, ParkingSpotBase, ParkingSpotUpdate,
    Reservation, ReservationCreate
)
from typing import List, Optional, Dict

class ParkingAPIClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.session = requests.Session()
        self.token = None

    # Authentication
    def signup(self, username: str, password: str, name: str, email: str) -> UserSignUp:
        response = self.session.post(
            f"{self.base_url}/auth/signup",
            json={"username": username, "password": password, "name": name, "email": email},
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        
        return UserSignUp(**response.json())

    def login(self, username: str, password: str) -> bool:
        response = self.session.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password},  # Form data for OAuth2PasswordRequestForm
            timeout=config.DEFAULT_TIMEOUT
        )
        if response.status_code == 200:
            token = Token(**response.json())
            self.token = token.access_token
            return True
        return False

    # User Endpoints
    def get_users(self, username: Optional[str] = None, email: Optional[str] = None, name: Optional[str] = None) -> ListResponse:
        params = {k: v for k, v in {"username": username, "email": email, "name": name}.items() if v is not None}
        response = self.session.get(
            f"{self.base_url}/users",
            params=params,
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        length = data.get("count")
        records = [User(**record) for record in data["records"]]
        
        return ListResponse(records=records, count=length)

    def get_user(self, user_id: str) -> User:
        response = self.session.get(
            f"{self.base_url}/users/{user_id}",
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return User(**response.json())

    def update_user(self, user_id: str, user_update: UserUpdate) -> User:
        payload = {k: v for k, v in user_update.__dict__.items() if v is not None}
        response = self.session.put(
            f"{self.base_url}/users/{user_id}",
            json=payload,
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return User(**response.json())

    def delete_user(self, user_id: str) -> bool:
        response = self.session.delete(
            f"{self.base_url}/users/{user_id}",
            timeout=config.DEFAULT_TIMEOUT
        )
        return response.status_code == 204

    # Spot Endpoints
    def get_spots(self, filters: Optional[Dict[str, tuple[str, str]]] = None) -> ListResponse:
        params = {}
        if filters:
            params["filter"] = [f"{field}:{op}:{val}" for field, (op, val) in filters.items()]
        response = self.session.get(
            f"{self.base_url}/spots",
            params=params,
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        length = data.get("count")
        records = [ParkingSpot(**record) for record in data["records"]]
        
        return ListResponse(records=records, count=length)

    def get_spot(self, spot_id: str) -> ParkingSpot:
        response = self.session.get(
            f"{self.base_url}/spots/{spot_id}",
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return ParkingSpot(**response.json())

    def create_spot(self, floor_level: int, spot_number: int, status: str = "vacant") -> ParkingSpot:
        response = self.session.post(
            f"{self.base_url}/spots",
            json={"floor_level": floor_level, "spot_number": spot_number, "status": status},
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return ParkingSpot(**response.json())

    def update_spot(self, spot_id: str, spot_update: ParkingSpotUpdate) -> ParkingSpot:
        payload = {k: v for k, v in spot_update.__dict__.items() if v is not None}
        response = self.session.put(
            f"{self.base_url}/spots/{spot_id}",
            json=payload,
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return ParkingSpot(**response.json())

    def delete_spot(self, spot_id: str) -> bool:
        response = self.session.delete(
            f"{self.base_url}/spots/{spot_id}",
            timeout=config.DEFAULT_TIMEOUT
        )
        return response.status_code == 204

    # Reservation Endpoints
    def get_reservations(self, filters: Optional[Dict[str, tuple[str, str]]] = None) -> ListResponse:
        params = {}
        if filters:
            params["filter"] = [f"{field}:{op}:{val}" for field, (op, val) in filters.items()]
        response = self.session.get(
            f"{self.base_url}/reservations",
            params=params,
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        length = data.get("count")
        records = [Reservation(**record) for record in data["records"]]
        
        return ListResponse(records=records, count=length)

    def get_reservation(self, reservation_id: str) -> Reservation:
        response = self.session.get(
            f"{self.base_url}/reservations/{reservation_id}",
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return Reservation(**response.json())

    def create_reservation(self, reservation: ReservationCreate) -> Reservation:
        response = self.session.post(
            f"{self.base_url}/reservations",
            json=reservation.__dict__,
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return Reservation(**response.json())

    def delete_reservation(self, reservation_id: str) -> bool:
        response = self.session.delete(
            f"{self.base_url}/reservations/{reservation_id}",
            timeout=config.DEFAULT_TIMEOUT
        )
        return response.status_code == 204
    
    
class PricingAPIClient:
    def __init__(self):
        self.base_url = config.PRICING_BASE_URL
        self.session = requests.Session()
        self.token = None
    
    def fetch_rate(self, timestamp: datetime) -> float:
        payload = {"timestamp": timestamp.isoformat()}
        
        response = self.session.post(
            url=f"{self.base_url}/calculate-rate",
            json=payload,
            timeout=config.DEFAULT_TIMEOUT
        )
        response.raise_for_status()
        return response.json().get("minute_rate")
    
    def fetch_total_price(self, start: datetime, end: datetime) -> float:
        
        rate = self.fetch_rate(start)
        time_diff_minutes = (end - start).total_seconds() / 60
        return round(time_diff_minutes * rate, 2)