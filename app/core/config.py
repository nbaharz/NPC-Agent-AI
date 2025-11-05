import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCES_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES","60"))

