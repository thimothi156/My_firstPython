from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import *
from authentication.jwt_auth import encode_token

router = APIRouter(
    prefix="",
    tags=["Authenticate"]
)

@router.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user or user.password != password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    encoded_jwt = encode_token({"id": user.id})
    return {"message": "Login successful", "token": encoded_jwt, "email": user.email, "id": user.id}

@router.post("/signup")
def signup(
    email: str,
    password: str,
    db: Session = Depends(get_db)
    ):
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        email=email,
        password=password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    encoded_jwt = encode_token({"id": new_user.id})
    return {"message": "Signup successful", "token": encoded_jwt, "email": new_user.email, "id": new_user.id}

