"""
File defining database schema.
"""

from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import Session
from datetime import datetime
from app.config.database import Base

class MachineData(Base):
    __tablename__ = "machine_data"

    id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String, index=True, nullable=False)
    topic = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

    @classmethod
    def create_entry(cls, session: Session, machine_name: str, topic: str, value: float, unit: str):
        entry = cls(machine_name=machine_name, topic=topic, value=value, unit=unit)
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry

    @classmethod
    def get_all_entries(cls, session: Session, machine_name: str):
        """Retrieve all entries for a specific machine."""
        return session.query(cls).filter(cls.machine_name == machine_name).all()

    @classmethod
    def delete_entry(cls, session: Session, entry_id: int):
        """Delete an entry by ID."""
        entry = session.query(cls).filter(cls.id == entry_id).first()
        if entry:
            session.delete(entry)
            session.commit()
        else:
            raise ValueError("Entry not found")
