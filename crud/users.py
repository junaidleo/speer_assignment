from sqlalchemy.orm import Session
from models.usersModel import UsersModel as User
from models.notesModel import NotesModel as Notes
from schemas import base as schema
from fastapi import HTTPException

def getAllUsers(db: Session):
    return db.query(User).all()

def getUserById(user_id: int,db: Session):
    return db.query(User).filter(User.id == user_id).first()

def getUserByUserName(user_name: str,db: Session):
    return db.query(User).filter(User.username == user_name).first()

def createUser(data: schema.UserCreate, db: Session):
    userItem = User(username = data.username, password = data.password)
    db.add(userItem)
    db.commit()
    db.refresh(userItem)
    return userItem

def deleteUser(id: int, db: Session):
    db.query(Notes).filter(Notes.created_by == id).delete()
    db.query(User).filter(User.userid == id).delete()
    db.commit()
    return {"message": "success"}
