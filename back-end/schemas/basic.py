from pydantic import BaseModel

class ORMModel(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True

class QueryModel(BaseModel):
    class Config:
        extra = "forbid"


