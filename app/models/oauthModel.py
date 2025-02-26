from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
    id: str
    username: str
    email: str
    password: str
    role: str

class UserInsertModel(BaseModel):
    username: str
    email: str
    password: str
    role: str

class UserRegisterModel(BaseModel):
    username: str
    email: str
    password: str

class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class TokenPayload(BaseModel):
    exp: int
    sub: str
    username: str
    role: str

class UserDataModel(BaseModel):
    username: str
    email: str

class UserAllDataModel(BaseModel):
    username: str
    email: str
    password: str