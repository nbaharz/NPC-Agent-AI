from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserLogin
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
class UserService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate):
        existing_user = UserRepository.get_by_email(db, user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        password_hash = pwd_context.hash(user_data.password)
        return UserRepository.create(db, user_data.username, user_data.email, password_hash)

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin):
        user = UserRepository.get_by_email(db, login_data.email)
        if not user:
            raise ValueError("No such user")
        if not pwd_context.verify(login_data.password, user.password):
            raise ValueError("You entered password wrong.")
        return user