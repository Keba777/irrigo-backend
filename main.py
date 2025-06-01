from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.controllers import products
from app.api.controllers import sensors

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(sensors.router, prefix="/api/v1", tags=["SensorData"])


@app.get("/")
def read_root():
    return {"messsage": "Hello"}
