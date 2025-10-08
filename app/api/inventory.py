# api/inventory.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db_session import SessionLocal
from app.database.models import Inventory

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/inventory/{user_id}")
def get_inventory(user_id: str, db: Session = Depends(get_db)):
    items = db.query(Inventory).filter(Inventory.user_id == user_id).all()
    return [
        {"item_id": i.item_id, "qty": i.qty, "meta": i.meta} for i in items
    ]
