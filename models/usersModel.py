from sqlalchemy import Column, DateTime, Integer, String, text
from db.init_db import Base

class UsersModel(Base):
    __tablename__ = 'users'

    userid = Column(Integer, primary_key = True, index = True, autoincrement = True)
    username = Column(String(500), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
