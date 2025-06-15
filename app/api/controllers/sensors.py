from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.sensor import (
    SensorDataCreate,
    SensorDataResponse,
    PumpControlRequest,
    PumpStatusResponse,
)
from app.crud.sensor import (
    create_sensor_data as crud_create_sensor_data,
    control_pump as crud_control_pump,
    get_latest_sensor_data as crud_get_latest_sensor_data,
    get_sensor_data_history as crud_get_sensor_data_history,
    get_pump_status as crud_get_pump_status,
)
from app.db.session import get_db

router = APIRouter()


@router.post("/sensor-data", response_model=SensorDataResponse)
def create_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db)):
    return crud_create_sensor_data(db, data)


@router.post("/pump/control", response_model=PumpStatusResponse)
def control_pump(request: PumpControlRequest, db: Session = Depends(get_db)):
    updated = crud_control_pump(db, request.command)
    if not updated:
        raise HTTPException(status_code=404, detail="No sensor data found")
    return PumpStatusResponse(
        status=updated.pump_status, last_updated=updated.updated_at
    )


@router.get("/pump/status", response_model=PumpStatusResponse)
def read_pump_status(db: Session = Depends(get_db)):
    latest = crud_get_pump_status(db)
    if not latest:
        raise HTTPException(status_code=404, detail="No pump status available")
    return PumpStatusResponse(status=latest.pump_status, last_updated=latest.updated_at)


@router.get("/sensor-history", response_model=List[SensorDataResponse])
def get_sensor_history(limit: int = 100, db: Session = Depends(get_db)):
    return crud_get_sensor_data_history(db, limit=limit)


@router.get("/latest-sensor-data", response_model=SensorDataResponse)
def read_latest_sensor_data(db: Session = Depends(get_db)):
    latest = crud_get_latest_sensor_data(db)
    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data available")
    return latest
