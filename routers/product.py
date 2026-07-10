from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Product, Category
from schemas.product import ProductCreate,ProductResponse
from typing import List,Optional
from authentication.jwt_auth import get_current_user


router = APIRouter(
    prefix="/products",
    tags=["Product"]
)

@router.post("/", response_model = ProductResponse)
def create(product: ProductCreate, db:Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if category is None :
        raise HTTPException(
            status_code=400, 
            detail="Category Not Found"
            )
    new_product = Product(name = product.name, price = product.price, stock = product.stock, category_id = product.category_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("", response_model = List[ProductResponse])
def list(name:Optional[str] = None, category:Optional[str] = None, db = Depends(get_db)):
    obj = db.query(Product)
    if category is not None:
        obj = obj.join(Category).filter(Category.name == category)
    elif  name is not None:
        obj = obj.filter(Product.name == name)
    return obj.all()

@router.get("/{product_id}", response_model = ProductResponse)
def show(product_id:int, db = Depends(get_db)): 
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )
    return product

@router.patch("/{product_id}", response_model = ProductResponse)
def update(product_id:int, product: ProductCreate, db = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )
    for key, value in product.dict().items():
        setattr(existing_product, key, value)
    db.commit()
    db.refresh(existing_product)
    return existing_product

@router.delete("/{product_id}")
def delete(product_id:int, db = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
    


      
    





    
    