from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Optional
import jwt
from config import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hash_password(password: str)-> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_time: Optional[timedelta]= None)-> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_time or timedelta(minutes= setting.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.JWT_SECRET_KEY, algorithm= setting.JWT_ALGORITHM)
    return encoded_jwt