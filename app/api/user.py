from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db_session import get_db
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.security import create_access_token
from app.core.config import ACCES_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse )
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = UserService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login", response_model=TokenResponse)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = UserService.authenticate_user(db, login_data)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "email": user.email},
        expires_delta=timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


