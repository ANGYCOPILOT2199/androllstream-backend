from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import videos
from app import oauth
from app import oauth_seznam

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix="/api")
app.include_router(oauth.router, prefix="/api")
app.include_router(oauth_seznam.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AndrollStream backend is running"}
