from langchain.tools import tool
from sqlalchemy.orm import Session
from app.database.models import WorldState, Inventory, Reputation
from app.database.db_session import SessionLocal
import uuid


@tool("inventory_add", return_direct=False)
def inventory_add_tool(user_id: str, item_name: str, qty: int = 1, meta: dict = None) -> str:
    """
    Kullanicinin envanterine yeni bir eşya ekler veya mevcut miktarini artirir.

    Args:
        user_id (str): Oyuncunun kimliği.
        item_name (str): Eklenecek eşyanin kimliği.
        qty (int, optional): Eşya miktari. Varsayilan = 1.
        meta (dict, optional): Eşya ile ilgili ek bilgiler (örn. nadirlik, özellikler).

    Returns:
        str: Eklenen eşyanin miktar ve adini belirten bir mesaj.

    Örnek:
        "1 adet key eklendi."
    """
    user_id = Inventory.user_id
    db = SessionLocal()
    row = db.query(Inventory).filter(Inventory.user_id == user_id, Inventory.item_name == item_name).first()
    if row:
        row.qty += qty
    else:
        row = Inventory(id=str(uuid.uuid4()), user_id=user_id, item_name=item_name, qty=qty, meta=meta or {})
        db.add(row)
    db.commit()
    db.close()
    return f"{qty} adet {item_name} eklendi."


@tool("inventory_remove", return_direct=False)
def inventory_remove_tool(user_id: str, item_id: str, qty: int = 1) -> str:
    """
    Kullanicinin envanterinden belirtilen miktarda esya cikarir.

    Args:
        user_id (str): Oyuncunun kimligi.
        item_id (str): Cikarilacak esyanin kimligi.
        qty (int, optional): Cikarilacak miktar. Varsayilan = 1.

    Returns:
        str: Cikarilan miktar ve esya adini belirten bir mesaj.
             Eger esya yoksa "Esya bulunamadi." mesaji doner.

    Ornek:
        "1 adet key cikarildi."
    """
    db = SessionLocal()
    row = db.query(Inventory).filter(Inventory.user_id == user_id, Inventory.id == item_id).first()
    if not row:
        db.close()
        return "Eşya bulunamadi."
    if row.qty <= qty:
        db.delete(row)
    else:
        row.qty -= qty
    db.commit()
    db.close()
    return f"{qty} adet {item_id} cikarildi."
