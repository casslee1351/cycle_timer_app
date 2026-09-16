from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.database import get_db
from app.security import get_current_user
from app import models, schemas

router = APIRouter(prefix="/cycles", tags=["cycles"])

@router.post("/", response_model=schemas.CycleRead)
def create_cycle(cycle: schemas.CycleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_cycle = models.Cycle(**cycle.model_dump())
    db.add(db_cycle)
    db.commit()
    db.refresh(db_cycle)
    return db_cycle

@router.get("/{cycle_id}", response_model=schemas.CycleRead)
def read_cycle(cycle_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_cycle = db.query(models.Cycle).filter(models.Cycle.id == cycle_id).first()
    if db_cycle is None:
        raise HTTPException(status_code=404, detail="Cycle not found")
    return db_cycle

@router.get("/", response_model=List[schemas.CycleRead])
def list_cycles(station_name: Optional[str] = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Cycle)
    if station_name is not None:
        query = query.filter(models.Cycle.station_name == station_name)
    return query.all()

@router.patch("/{cycle_id}", response_model=schemas.CycleRead)
def update_cycle(cycle_id: int, update: schemas.CycleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_cycle = db.query(models.Cycle).filter(models.Cycle.id == cycle_id).first()
    if db_cycle is None:
        raise HTTPException(status_code=404, detail="Cycle not found")
    
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cycle, field, value)
    db.commit()
    db.refresh(db_cycle)
    return db_cycle

@router.get("analytics/average-by-station", response_model=List[schemas.StationAverage])
def average_cycle_time_by_station(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    duration_seconds = func.avg(func.julianday(models.Cycle.end_time) - func.julianday(models.Cycle.start_time)) * 86400.0

    results = db.query(models.Cycle.station_name, duration_seconds.label("average_cycle_seconds"), func.count(models.Cycle.id).label("completed_cycle_count")) \
                .filter(models.Cycle.end_time.isnot(None)) \
                .group_by(models.Cycle.station_name).all()

    return results

@router.post("/{cycle_id}/laps", response_model=schemas.LapRead)
def create_lap(cycle_id: int, lap: schemas.LapCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_cycle = db.query(models.Cycle).filter(models.Cycle.id == cycle_id).first()
    if db_cycle is None:
        raise HTTPException(status_code=404, detail="Cycle not found")
    
    db_lap = models.Lap(cycle_id=cycle_id, recorded_at=datetime.now(timezone.utc), note=lap.note)
    db.add(db_lap)
    db.commit()
    db.refresh(db_lap)
    return db_lap

@router.get("/{cycle_id}/laps", response_model=List[schemas.LapRead])
def list_laps(cycle_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_cycle = db.query(models.Cycle).filter(models.Cycle.id == cycle_id).first()
    if db_cycle is None:
        raise HTTPException(status_code=404, detail="Cycle not found")
    
    return db.query(models.Lap).filter(models.Lap.cycle_id == cycle_id).all()