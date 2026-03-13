from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True)
    title = Column(String)
    thumbnail_url = Column(String)
    video_url = Column(String)
    duration = Column(Integer)  # Duration in seconds
