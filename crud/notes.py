import datetime
from sqlalchemy.orm import Session
from models.usersModel import UsersModel as User
from models.notesModel import NotesModel as Notes
from sqlalchemy import or_
from schemas import base as schema
from fastapi import HTTPException

def getAllNotesByUser(userid: int, db: Session):
    return db.query(Notes).filter(or_(Notes.shared_with.contains([userid]),Notes.created_by == userid)).all()

def getNotesById(id: int, userid: int,  db: Session):
    return db.query(Notes).filter(Notes.created_by == userid).filter(Notes.id == id).first()

def getNotesByStr(user_id: int, search_string: str,db: Session):
    return db.query(Notes).filter(Notes.created_by == user_id).filter(Notes.notes.match(search_string)).all()

def createNote(user_id: int, data: schema.NoteBase, db: Session):
    note = Notes(notes = data.notes, created_by = user_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def updateNote(userid: int, data: schema.Note, id: int, db: Session):
    note = db.query(Notes).filter(Notes.id == id).filter(Notes.created_by == userid)
    notedata = note.first()
    if not notedata:
        raise HTTPException(status_code = 404, detail = "Todo not found")
    data.updated_at = datetime.datetime.now()
    note.filter(Notes.id == id).update(data.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(notedata)
    return notedata

def deleteNote(userid: int, id: int, db: Session):
    db.query(Notes).filter(Notes.id == id).filter(Notes.created_by == userid).delete()
    db.commit()
    return {"message": "success"}

def shareNote(userid: int, note_id: int, receiver_id: int, db: Session):
    if userid == receiver_id:
        raise HTTPException(status_code = 400, detail = "Cannot share with self")
    note = db.query(Notes).filter(Notes.id == note_id).filter(Notes.created_by == userid).first()
    shared_ids = note.shared_with
    if not shared_ids:
        shared_ids = []
    if receiver_id in shared_ids:
        raise HTTPException(status_code = 400, detail = "Already shared with this user")
    shared_ids.append(receiver_id)
    note.shared_with = shared_ids
    db.commit()
    db.refresh(note)
    return note

