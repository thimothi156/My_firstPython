from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import *
from schemas.user_profile import UserProfileResponse, UserProfileCreate
from typing import List
from authentication.jwt_auth import get_current_user


router = APIRouter(
    prefix="/user_profile",
    tags=["UserProfile"]
)

@router.post("/", response_model = UserProfileResponse)
def create(user_profile: UserProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_profile_exists = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if user_profile_exists:
        raise HTTPException(
            status_code=400,
            detail="User profile already exists"
        )
    new_profile = UserProfile(first_name = user_profile.first_name, 
                              last_name = user_profile.last_name,
                              phone = user_profile.phone,
                              user = current_user
                            )
   
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


@router.patch("/{user_id}", response_model=UserProfileResponse)
def update(user_id: int, user_profile: UserProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User profile not found"
        )
    for key, value in user_profile.dict().items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

