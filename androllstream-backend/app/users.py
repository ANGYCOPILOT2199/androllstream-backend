import uuid
import hashlib
from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.models import User

router = APIRouter()

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if not SessionLocal:
        return {"error": "Database not configured"}

    db: Session = next(get_db())

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return {"error": "Username already exists"}

    user = User(
        id=str(uuid.uuid4()),
        username=username,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": user.id, "username": user.username}

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if not SessionLocal:
        return {"error": "Database not configured"}

    db: Session = next(get_db())

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return {"error": "Invalid username or password"}

    if user.password_hash != hash_password(password):
        return {"error": "Invalid username or password"}

    return {"id": user.id, "username": user.username}
