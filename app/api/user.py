from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse )
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = UserService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_model=UserResponse)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, login_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user


