from fastapi import HTTPException, status
from app.data_access.auth_dao import auth_user
from app.models.oauthModel import UserModel
from app.utils import verify_password
from pymongo.database import Database

def login_user(username: str, password: str, db: Database) -> UserModel:
    user = auth_user(username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    hashed_pass = user.password
    if not verify_password(password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return user

    