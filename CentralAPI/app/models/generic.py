from typing import List, TypeVar, Generic
from pydantic import BaseModel, computed_field
T = TypeVar("T")

class ListResponse(BaseModel, Generic[T]):
    records: List[T]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.records)
    

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None