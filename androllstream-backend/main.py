from fastapi import FastAPI
from app import videos, oauth

app = FastAPI()

app.include_router(videos.router, prefix="/api")
app.include_router(oauth.router, prefix="/api")
