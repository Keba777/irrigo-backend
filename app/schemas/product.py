# app/schemas/product.py

from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    url: str


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    url: Optional[str] = None


class Product(ProductBase):
    id: int
    current_price: float
    price_history: List[float]

    class Config:
        from_attributes = True
