from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from routes.deps import SECRET_KEY, ALGORITHM
from crud import users
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt_hash(password):
    return pwd_context.hash(password)

def verify_pass(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def authenticate_user(username, password, db):
    user_data = users.getUserByUserName(username, db)
    if not user_data or not verify_pass(password, user_data.password):
        return False
    return user_data

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
