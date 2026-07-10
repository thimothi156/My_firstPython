from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cart, Product
from schemas.cart import CartCreate, CartResponse
from typing import List