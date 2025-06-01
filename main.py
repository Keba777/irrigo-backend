from fastapi import FastAPI
from app.db.session import Base, engine
from app.api.controllers import products

app = FastAPI()

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app.include_router(products.router)


@app.get("/")
def read_root():
    return {"messsage": "Hello"}
