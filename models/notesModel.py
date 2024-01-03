from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.dialects import postgresql
from db.init_db import Base

class NotesModel(Base):
    __tablename__ = 'notes'

    id = Column(Integer, autoincrement= True, primary_key=True, index=True)
    notes = Column(String(500), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    created_by = Column(Integer, nullable=False)
    shared_with = Column(postgresql.ARRAY(Integer), nullable=True, default=[])
