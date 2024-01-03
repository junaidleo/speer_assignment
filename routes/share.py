from fastapi import FastAPI, HTTPException, Depends, status
from fastapi import APIRouter
from .deps import get_current_user, get_db
from typing import Annotated
from sqlalchemy.orm import Session
from crud import notes
from schemas import base as schema
import models

router = APIRouter()

@router.get("/")
def read_notes(
    q: str,
    current_user: models.UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return notes.getNotesByStr(current_user.userid, q, db)
