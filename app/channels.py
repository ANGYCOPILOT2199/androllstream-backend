import uuid
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import Channel, User

router = APIRouter()

@router.post("/create")
def create_channel(
    owner_id: str = Form(...),
    name: str = Form(...),
    description: str = Form("")
):
    if not SessionLocal:
        return {"error": "Database not configured"}

    db: Session = next(get_db())

    owner = db.query(User).filter(User.id == owner_id).first()
    if not owner:
        return {"error": "Owner not found"}

    existing = db.query(Channel).filter(Channel.name == name).first()
    if existing:
        return {"error": "Channel name already exists"}

    channel = Channel(
        id=str(uuid.uuid4()),
        owner_id=owner_id,
        name=name,
        description=description
    )

    db.add(channel)
    db.commit()
    db.refresh(channel)

    return {
        "id": channel.id,
        "name": channel.name,
        "description": channel.description,
        "owner_id": channel.owner_id
    }

@router.get("/{channel_id}")
def get_channel(channel_id: str):
    if not SessionLocal:
        return {"error": "Database not configured"}

    db: Session = next(get_db())

    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        return {"error": "Channel not found"}

    return {
        "id": channel.id,
        "name": channel.name,
        "description": channel.description,
        "owner_id": channel.owner_id,
        "created_at": channel.created_at
    }

@router.get("/user/{owner_id}")
def get_user_channels(owner_id: str):
    if not SessionLocal:
        return {"error": "Database not configured"}

    db: Session = next(get_db())

    channels = db.query(Channel).filter(Channel.owner_id == owner_id).all()

    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "created_at": c.created_at
        }
        for c in channels
    ]
