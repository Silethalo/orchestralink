"""
File containing routing logic.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import MachineData
from app.config.database import Database

router = APIRouter()

def get_db():
    """Dependency to provide a database session."""
    try:
        db = Database.get_session()
        yield db
    finally:
        db.close()

@router.get("/machine-data")
def get_machine_data(machine_name: str, db: Session = Depends(get_db)):
    data = MachineData.get_all_entries(db, machine_name)
    if not data:
        raise HTTPException(status_code=404, detail="Machine data not found")
    return {"data": data}

@router.post("/machine-data")
def add_machine_data(machine_name: str, topic: str, value: float, unit: str, db: Session = Depends(get_db)):
    entry = MachineData.create_entry(db, machine_name, topic, value, unit)
    return {"message": "Data added successfully", "data": entry}

@router.delete("/machine-data/{entry_id}")
def delete_machine_data(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(MachineData).filter(MachineData.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return {"message": "Entry deleted successfully"}

