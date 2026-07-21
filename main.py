from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Video

router = APIRouter(prefix="/videos")

@router.get("/all")
def get_all_videos(db: Session = Depends(get_db)):
    return db.query(Video).all()
