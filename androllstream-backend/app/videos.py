import os
import uuid
import subprocess
from fastapi import APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import Video, Channel

router = APIRouter()

VIDEO_DIR = "static/videos"

@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(""),
    channel_id: str = Form(...)
):
    video_id = str(uuid.uuid4())
    video_path = f"{VIDEO_DIR}/{video_id}"
    os.makedirs(video_path, exist_ok=True)

    original_file = f"{video_path}/input.mp4"
    with open(original_file, "wb") as f:
        f.write(await file.read())

    playlist_path = f"{video_path}/playlist.m3u8"

    subprocess.run([
        "ffmpeg",
        "-i", original_file,
        "-codec:", "copy",
        "-start_number", "0",
        "-hls_time", "5",
        "-hls_list_size", "0",
        "-f", "hls",
        playlist_path
    ])

    if SessionLocal:
        db: Session = next(get_db())

        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        if not channel:
            return {"error": "Channel not found"}

        video = Video(
            id=video_id,
            title=title,
            description=description,
            filename=file.filename,
            playlist_path=playlist_path,
            channel_id=channel_id
        )

        db.add(video)
        db.commit()
        db.refresh(video)

    return {
        "video_id": video_id,
        "title": title,
        "stream_url": f"/api/stream/{video_id}/playlist.m3u8"
    }
