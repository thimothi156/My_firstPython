from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import get_db,Session
from models import Order
from schemas.order import OrderCreate, OrderResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"])

@router.post("/",response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(user_id=order.user_id, product_id=order.product_id, quantity=order.quantity)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order