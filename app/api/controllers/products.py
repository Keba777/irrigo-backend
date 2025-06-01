from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, Product
from app.crud.product import create_product, get_products, get_product_by_id, update_product, delete_product

router = APIRouter()


@router.post("/products", response_model=Product)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        # Scrape the price
        scraped_price = scraped_price(product.url)  # or scrape_price_with_bs4
        product.current_price = scraped_price
        return create_product(db, product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")



@router.get("/products", response_model=list[Product])
def get_products_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products(db, skip, limit)


@router.get("/products/{product_id}", response_model=Product)
def get_product_by_id_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=Product)
def update_product_endpoint(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/products/{product_id}", response_model=dict)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}
