from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,selectinload
from database import get_db
from models import Category
from schemas.category import CategoryData
from typing import List
from authentication.jwt_auth import get_current_user


router = APIRouter(
    prefix="/categories",
    tags=["Category"]
)


@router.post("/", response_model = CategoryData)
def create(category: CategoryData, db:Session = Depends(get_db)):
    new_category = Category(name = category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("", response_model = List[CategoryData])
def list(db = Depends(get_db)):
    return db.query(Category).all()

@router.get("/{category_id}", response_model = CategoryData)
def show(category_id:int, db = Depends(get_db)): 
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
    return category

@router.patch("/{category_id}", response_model = CategoryData)
def update(category_id:int, category: CategoryData, db = Depends(get_db)): 
    existing_category = db.query(Category).filter(Category.id == category_id).first()
    if existing_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
    for key, value in category.dict().items():
        setattr(existing_category, key, value)
    db.commit()
    db.refresh(existing_category)
    return existing_category

@router.delete("/{category_id}")
def delete(category_id:int, db = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}

@router.get("/tree",response_model = List[CategoryData])
def get_category_tree(db = Depends(get_db)):
    categories = (
        db.query(Category)
        .options(selectinload(Category.sub_categories))
        .filter(Category.parent_id == None)
        .all()
    )
    return categories
    pass