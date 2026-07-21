from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Comment(BaseModel):
    video_id: int
    username: str
    text: str

@router.post("/")
def add_comment(data: Comment):
    return {"message": "Comment added", "comment": data}

@router.get("/{video_id}")
def get_comments(video_id: int):
    return {"video_id": video_id, "comments": []}
