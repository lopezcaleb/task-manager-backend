from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.database import get_db
from app.models.oauthModel import TokenPayload, UserDataModel, UserRegisterModel, UserUpdateModel
from app.services.userServices import Delte_user, Update_user, get_current_user, register_user
from app.utils import verify_auth, verify_rol
from pymongo.database import Database

routerUser = APIRouter()
db = get_db()

@routerUser.get('/', tags=["user"], summary='Get data user by auth token', status_code=status.HTTP_200_OK, response_model=UserDataModel)
def get_me(tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    verify_rol(["admin", "user"], tokenData.role)
    user: UserDataModel = get_current_user(tokenData.sub, db)
    return user

@routerUser.post("/", tags=["user"],status_code=status.HTTP_201_CREATED, summary="Register new user")
def register(user: UserRegisterModel, db: Database = Depends(get_db)):
    try:
        result = register_user(user, db)
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@routerUser.put('/', tags=["user"], summary="Update user", status_code=status.HTTP_200_OK)
def update(user: UserUpdateModel, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        result = Update_user(tokenData.sub, user, db)
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@routerUser.delete('/', tags=["user"], summary="Delete user", status_code=status.HTTP_200_OK)
def delete (tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        result = Delte_user(tokenData.sub, db)
        return result
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)