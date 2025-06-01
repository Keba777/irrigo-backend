from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
import json


def create_product(db: Session, product: ProductCreate) -> Product:
    """
    Create a new product with user-provided data.
    """
    # Initialize price history from current_price
    price_history = [product.current_price]

    db_product = Product(
        name=product.name,
        url=product.url,
        current_price=product.current_price,
        price_history=json.dumps(price_history),  # Store as JSON
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 10):
    """
    Get a list of all products.
    """
    return db.query(Product).offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int) -> Product:
    """
    Get a single product by its ID.
    """
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(
    db: Session, product_id: int, product_update: ProductUpdate
) -> Product:
    """
    Update an existing product with new data.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None

    if product_update.name is not None:
        db_product.name = product_update.name
    if product_update.url is not None:
        db_product.url = product_update.url
    if product_update.current_price is not None:
        db_product.current_price = product_update.current_price
    if product_update.price_history is not None:
        db_product.price_history = json.dumps(product_update.price_history)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """
    Delete a product by its ID.
    """
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return False

    db.delete(db_product)
    db.commit()
    return True
