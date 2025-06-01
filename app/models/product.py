from sqlalchemy import Column, Integer, String, Numeric, JSON, CheckConstraint
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, index=True)
    current_price = Column(Numeric(10, 2), index=True)  
    price_history = Column(JSON, nullable=True)  

    __table_args__ = (
        CheckConstraint("url ~* '^https?://'", name="url_check_http"),
    )
