from pydantic import BaseModel
from datetime import datetime

class TrendsRunCreate(BaseModel):
    trend1: str | None = None
    trend2: str | None = None
    trend3: str | None = None
    trend4: str | None = None
    trend5: str | None = None
    ip_address: str | None = None

class TrendsRunOut(TrendsRunCreate):
    id: str
    run_time: datetime

    class Config:
        from_attributes = True
