from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.database.models import WorldState, Inventory, Reputation

router = APIRouter()

def _rows(rows):
    out = []
    for r in rows:
        d = {c.name: getattr(r, c.name) for c in r.__table__.columns}
        # datetime → iso
        if "updated_at" in d and d["updated_at"]:
            d["updated_at"] = d["updated_at"].isoformat()
        out.append(d)
    return out

@router.get("/world_state")
def list_world_state(db: Session = Depends(get_db)):
    rows = db.query(WorldState).all()
    return _rows(rows)

@router.get("/inventory/{user_id}")
def list_inventory(user_id: str, db: Session = Depends(get_db)):
    rows = db.query(Inventory).filter(Inventory.user_id == user_id).all()
    return _rows(rows)

@router.get("/reputation/{user_id}")
def list_reputation(user_id: str, db: Session = Depends(get_db)):
    rows = db.query(Reputation).filter(Reputation.user_id == user_id).all()
    return _rows(rows)
