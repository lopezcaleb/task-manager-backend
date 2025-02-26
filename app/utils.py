import os
from datetime import datetime, timedelta
from typing import Union, Any
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.hash import pbkdf2_sha256
import os
from dotenv import load_dotenv
from pydantic import ValidationError
from app.models.oauthModel import TokenPayload

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')    # should be kept secret

def hash_pass(password:str):
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
     return pbkdf2_sha256.verify(password, hashed_pass)

def create_access_token(subject: Union[str, Any],username: Union[str, Any], role: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject), "role": role, "username": username}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any],username: Union[str, Any], role: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject), "role": role, "username": username}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

# Validar autenticacion
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/auth",
    scheme_name="JWT"
)

def verify_auth(token: str = Depends(reuseable_oauth)) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token_data
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def verify_rol(allowed_roles: list, role: str):
    if role not in allowed_roles:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Rol is not valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def validate_formad_id(mongo_id):
    try:
        ObjectId(mongo_id)
        return True
    except:
        return False