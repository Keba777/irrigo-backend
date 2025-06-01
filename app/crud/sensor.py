from sqlalchemy.orm import Session
from app.models.sensor import SensorData
from app.schemas.sensor import SensorDataCreate, SensorDataUpdate
from datetime import datetime


def create_sensor_data(db: Session, sensor_data: SensorDataCreate) -> SensorData:
    """
    Create a new sensor data record.
    """
    db_sensor = SensorData(
        sensor_type=sensor_data.sensor_type,
        temperature=sensor_data.temperature,
        humidity=sensor_data.humidity,
        moisture_percentage=sensor_data.moisture_percentage,
        water_level=sensor_data.water_level,
    )
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def get_sensor_data(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of sensor data entries.
    """
    return db.query(SensorData).offset(skip).limit(limit).all()


def get_sensor_data_by_id(db: Session, sensor_id: int) -> SensorData:
    """
    Retrieve a single sensor data record by ID.
    """
    return db.query(SensorData).filter(SensorData.id == sensor_id).first()


def update_sensor_data(
    db: Session, sensor_id: int, sensor_update: SensorDataUpdate
) -> SensorData:
    """
    Update an existing sensor data entry.
    """
    db_sensor = db.query(SensorData).filter(SensorData.id == sensor_id).first()
    if not db_sensor:
        return None

    if sensor_update.temperature is not None:
        db_sensor.temperature = sensor_update.temperature
    if sensor_update.humidity is not None:
        db_sensor.humidity = sensor_update.humidity
    if sensor_update.moisture_percentage is not None:
        db_sensor.moisture_percentage = sensor_update.moisture_percentage
    if sensor_update.water_level is not None:
        db_sensor.water_level = sensor_update.water_level

    db_sensor.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_sensor)
    return db_sensor


def delete_sensor_data(db: Session, sensor_id: int) -> bool:
    """
    Delete a sensor data record by ID.
    """
    db_sensor = db.query(SensorData).filter(SensorData.id == sensor_id).first()
    if not db_sensor:
        return False

    db.delete(db_sensor)
    db.commit()
    return True
