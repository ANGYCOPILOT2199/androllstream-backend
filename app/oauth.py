from fastapi import APIRouter

router = APIRouter(prefix="/oauth2")

@router.get("/authorize")
def oauth_authorize():
    return {
        "message": "OAuth 2.0 authorization endpoint",
        "authorize_url": "https://example.com/oauth2/authorize"
    }
