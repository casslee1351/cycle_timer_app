from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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