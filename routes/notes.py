from fastapi import FastAPI, HTTPException, Depends, status
from fastapi import APIRouter
from .deps import get_current_user, get_db
from typing import Annotated
from sqlalchemy.orm import Session
from crud import notes, users
from schemas import base as schema
import models

router = APIRouter()

@router.get("/")
def read_notes(
    current_user: models.UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return notes.getAllNotesByUser(current_user.userid, db)

@router.get("/{id}")
def read_notes_by_id(
    id: int,
    current_user: models.UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return notes.getNotesById(id, current_user.userid, db)

@router.post("/")
def post_notes(
    note_in: schema.NoteBase,
    current_user: models.UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return notes.createNote(
        current_user.userid,
        note_in,
        db
    )

@router.put("/{id}")
def update_notes(
    id: int,
    note_in: schema.NoteBase,
    current_user: models.UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note_updated = schema.Note(notes=note_in.notes)
    return notes.updateNote(
        current_user.userid,
        note_updated,
        id,
        db
    )

@router.delete("/{id}")
def delete_notes(
    id: int,
    current_user: models.UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return notes.deleteNote(
        current_user.userid,
        id,
        db
    )

@router.post("/{id}/share")
def share_notes(
    id: int,
    share_with: schema.UserBase,
    current_user: models.UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    receiver_user = users.getUserByUserName(share_with.username, db)
    return notes.shareNote(
        current_user.userid,
        id,
        receiver_user.userid,
        db
    )    
