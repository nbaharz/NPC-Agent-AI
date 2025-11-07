# api/inventory.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db_session import SessionLocal
from app.database.models import Inventory
from app.services.token_service import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/inventory")
def get_inventory(user_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    items = db.query(Inventory).filter(Inventory.user_id == current_user.id).all()
    return [
        {"id": i.id, "qty": i.qty, "meta": i.meta} for i in items
    ]
