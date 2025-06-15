import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine
from app.api.controllers import products
from app.api.controllers import sensors
import uvicorn

app = FastAPI()

# Enable CORS (Critical for ESP32 communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (adjust for production)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Include your existing routers
app.include_router(sensors.router, prefix="/api/v1", tags=["SensorData"])


@app.get("/")
def read_root():
    return {
        "message": " Backend is running",
        "local_ip": "192.168.196.89",  # Explicitly show the expected IP
        "endpoints": {
            "sensor_data": "/api/v1/sensor-data",
            "pump_control": "/api/v1/pump/control",
            "pump_status": "/api/v1/pump/status",
        },
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))

    # Explicit configuration for local network access
    uvicorn.run(
        app,
        host="0.0.0.0",  # Crucial - makes server available on all network interfaces
        port=port,
        reload=True,  # Optional: Auto-reload during development
    )
