from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CycleBase(BaseModel):
    station_name: str = Field(..., example="Which station/process step this cycle belongs to")
    start_time: datetime
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

class CycleCreate(CycleBase):
    pass

class CycleRead(CycleBase):
    id: int

    class Config:
        from_attributes = True

class CycleUpdate(BaseModel):
    end_time: Optional[datetime] = None
    notes: Optional[str] = None