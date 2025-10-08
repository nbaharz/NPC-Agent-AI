from sqlalchemy.orm import Session
from app.database.models import User

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(db: Session, id: str):
        return db.query(User).filter(User.id == id).first()
    
    @staticmethod
    def create(db: Session, username: str, email: str, password_hash: str):
        new_user = User(username=username, email=email, password=password_hash)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    