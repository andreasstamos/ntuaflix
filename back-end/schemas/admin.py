from typing import Optional
from pydantic import BaseModel

class HealthCheckObject(BaseModel):
    status: str
    dataconnection: str

class ResetAllObject(BaseModel):
    status: str

class UploadFileObject(BaseModel):
    status: str
    reason: Optional[str] = None

