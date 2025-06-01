from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.sensor import SensorDataCreate, SensorDataUpdate, SensorData
from app.crud.sensor import (
    create_sensor_data,
    get_sensor_data,
    get_sensor_data_by_id,
    update_sensor_data,
    delete_sensor_data,
)

router = APIRouter()


@router.post("/sensors", response_model=SensorData)
def create_sensor_data_endpoint(
    sensor: SensorDataCreate, db: Session = Depends(get_db)
):
    try:
        return create_sensor_data(db, sensor)
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/sensors", response_model=list[SensorData])
def get_sensor_data_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_sensor_data(db, skip, limit)


@router.get("/sensors/{sensor_id}", response_model=SensorData)
def get_sensor_data_by_id_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    sensor = get_sensor_data_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor data not found")
    return sensor


@router.put("/sensors/{sensor_id}", response_model=SensorData)
def update_sensor_data_endpoint(
    sensor_id: int, sensor_update: SensorDataUpdate, db: Session = Depends(get_db)
):
    sensor = update_sensor_data(db, sensor_id, sensor_update)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor data not found")
    return sensor


@router.delete("/sensors/{sensor_id}", response_model=dict)
def delete_sensor_data_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    success = delete_sensor_data(db, sensor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sensor data not found")
    return {"detail": "Sensor data deleted successfully"}
