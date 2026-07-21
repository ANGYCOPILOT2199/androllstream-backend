from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Channel(Base):
    __tablename__ = "channels"
    id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, ForeignKey("users.id"))
    name = Column(String, unique=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    filename = Column(String)
    playlist_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    channel_id = Column(String, ForeignKey("channels.id"))
