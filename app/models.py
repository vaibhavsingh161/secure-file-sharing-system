from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)
    role = Column(String)  # 'ops' or 'client'

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filepath = Column(String)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
