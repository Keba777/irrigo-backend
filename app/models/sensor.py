from sqlalchemy import Column, Integer, Float, Enum as SqlEnum, DateTime
from sqlalchemy.sql import func
from enum import Enum
from app.db.session import Base


class SensorType(str, Enum):
    TEMPERATURE_HUMIDITY = "temperature_humidity"
    SOIL_MOISTURE = "soil_moisture"
    WATER_LEVEL = "water_level"


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_type = Column(SqlEnum(SensorType), nullable=False, index=True)

    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    moisture_percentage = Column(Float, nullable=True)
    water_level = Column(Float, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
