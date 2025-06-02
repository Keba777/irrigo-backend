from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.sensor import SensorType


# Base schema shared by Create/Update/Read
class SensorDataBase(BaseModel):
    sensor_type: SensorType
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    moisture_percentage: Optional[float] = None
    water_level: Optional[float] = None


# Schema for creating new sensor data
class SensorDataCreate(SensorDataBase):
    pass


# Schema for updating existing sensor data
class SensorDataUpdate(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    moisture_percentage: Optional[float] = None
    water_level: Optional[float] = None


# Schema for response/output with ORM support
class SensorData(SensorDataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
