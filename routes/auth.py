from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import base as schema
from sqlalchemy.orm import Session
from crud import users
from .deps import get_db, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from helpers import *
from datetime import timedelta

router = APIRouter()


@router.post("/signup")
def signup(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = users.getUserByUserName(user_data.username, db)
    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Username already exists")
    user_data.password = bcrypt_hash(user_data.password)
    user_data = users.createUser(user_data, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}