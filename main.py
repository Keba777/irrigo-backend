import os
from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.controllers import products
from app.api.controllers import sensors
import uvicorn

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(sensors.router, prefix="/api/v1", tags=["SensorData"])


@app.get("/")
def read_root():
    return {"message": "Hello"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
