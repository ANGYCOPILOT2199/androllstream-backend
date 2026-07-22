from fastapi import APIRouter, Request, Depends
import requests
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

SEZNAM_CLIENT_ID = "YOUR_SEZNAM_CLIENT_ID"
SEZNAM_CLIENT_SECRET = "YOUR_SEZNAM_CLIENT_SECRET"
SEZNAM_REDIRECT_URI = "https://androllstream-backend-1.onrender.com/api/oauth2/seznam/callback"

router = APIRouter(prefix="/oauth2/seznam")

@router.get("/authorize")
def seznam_authorize():
    url = (
        "https://login.szn.cz/api/v1/oauth/authorize"
        f"?client_id={SEZNAM_CLIENT_ID}"
        f"&redirect_uri={SEZNAM_REDIRECT_URI}"
        "&response_type=code"
        "&scope=identity"
    )
    return {"authorize_url": url}

@router.get("/callback")
def seznam_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")

    token_url = "https://login.szn.cz/api/v1/oauth/token"
    token_data = {
        "code": code,
        "client_id": SEZNAM_CLIENT_ID,
        "client_secret": SEZNAM_CLIENT_SECRET,
        "redirect_uri": SEZNAM_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    token_response = requests.post(token_url, data=token_data).json()
    access_token = token_response.get("access_token")

    user_info = requests.get(
        "https://login.szn.cz/api/v1/user",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    email = user_info.get("email")
    name = user_info.get("name")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, username=name, password="oauth-seznam")
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"message": "Seznam login successful", "email": email, "username": name}
