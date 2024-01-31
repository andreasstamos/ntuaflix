from pydantic import BaseModel

from datetime import date

class ORMModel(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True

class QueryModel(BaseModel):
    class Config:
        extra = "forbid"


class UserObject(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    birtday: date
    