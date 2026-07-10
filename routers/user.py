from fastapi import APIRouter, Depends, HTTPException,Header
from sqlalchemy.orm import Session
from database import get_db
from models import *
from schemas.user import UserCreate, UserResponse,DashboardResponse
from typing import List
from authentication.jwt_auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Get all users
@router.get("/", response_model = List[UserResponse])
def list(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(User).all()


# Get single user
@router.get("/{user_id}", response_model=UserResponse)
def show(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put("/{user_id}", response_model=UserResponse)
def update(user_id: int, user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    for key, value in user_data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("")
def delete_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(User).delete()
    db.commit()
    return {"message": "All users deleted successfully"}

@router.delete("/{user_id}")
def user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User is not found"
        )
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


