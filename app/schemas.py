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

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class StationAverage(BaseModel):
    station_name: str
    average_cycle_seconds: float
    completed_cycle_count: int

class LapCreate(BaseModel):
    note: Optional[str] = None

class LapRead(BaseModel):
    id: int
    cycle_id: int
    recorded_at: datetime
    note: Optional[str] = None

    class Config:
        from_attributes = True