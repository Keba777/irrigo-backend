from sqlalchemy.orm import Session
from app.models.sensor import SensorData
from app.schemas.sensor import SensorDataCreate
from typing import List, Optional


def create_sensor_data(db: Session, data: SensorDataCreate) -> SensorData:
    db_data = SensorData(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_latest_sensor_data(db: Session) -> Optional[SensorData]:
    return db.query(SensorData).order_by(SensorData.created_at.desc()).first()


def get_sensor_data_history(db: Session, limit: int = 100) -> List[SensorData]:
    return (
        db.query(SensorData).order_by(SensorData.created_at.desc()).limit(limit).all()
    )


def control_pump(db: Session, command: str) -> Optional[SensorData]:
    latest = get_latest_sensor_data(db)
    if latest:
        latest.pump_status = command
        db.commit()
        db.refresh(latest)
        return latest
    return None


def get_pump_status(db: Session) -> Optional[SensorData]:
    return get_latest_sensor_data(db)