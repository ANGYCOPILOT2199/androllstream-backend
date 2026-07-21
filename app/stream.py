import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

VIDEO_DIR = "static/videos"

@router.get("/{video_id}/playlist.m3u8")
def stream_playlist(video_id: str):
    playlist_path = f"{VIDEO_DIR}/{video_id}/playlist.m3u8"
    if not os.path.exists(playlist_path):
        return {"error": "Playlist not found"}
    return FileResponse(playlist_path)
