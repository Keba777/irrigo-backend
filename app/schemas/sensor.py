from pydantic import BaseModel
from datetime import datetime
from typing import Literal


# ========== SENSOR DATA SCHEMAS ==========


class SensorDataBase(BaseModel):
    temperature: float
    humidity: float
    soil_moisture: float
    pump_status: Literal["ON", "OFF"]


class SensorDataCreate(SensorDataBase):
    pass


class SensorDataResponse(SensorDataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========== PUMP CONTROL SCHEMAS ==========


class PumpControlRequest(BaseModel):
    command: Literal["ON", "OFF"]


class PumpStatusResponse(BaseModel):
    status: Literal["ON", "OFF"]
    last_updated: datetime

    class Config:
        from_attributes = True
