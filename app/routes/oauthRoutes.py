from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.services.oauthServices import login_user
from app.utils import create_access_token, create_refresh_token
from pymongo.database import Database

routerOauth = APIRouter()
db = get_db()

@routerOauth.post('/', tags=["auth"], summary="Create access and refresh tokens for user", status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),  db: Database = Depends(get_db)):
    try:
        user = login_user(form_data.username, form_data.password, db)

        return {
            "access_token": create_access_token(user.id, user.username, user.role),
            "refresh_token": create_refresh_token(user.id, user.username, user.role),
        }
    
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        