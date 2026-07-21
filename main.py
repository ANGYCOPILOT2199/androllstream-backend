from fastapi import FastAPI
from app.users import router as users_router
from app.channels import router as channels_router
from app.videos import router as videos_router
from app.stream import router as stream_router

app = FastAPI()

app.include_router(users_router, prefix="/api/users")
app.include_router(channels_router, prefix="/api/channels")
app.include_router(videos_router, prefix="/api/videos")
app.include_router(stream_router, prefix="/api/stream")
app.include_router(videos.router, prefix="/api")