from fastapi import  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pymongo.database import Database
from app.data_access.user_dao import delte_user, get_user_by_id, get_user_by_username, insert_user, update_user
from app.models.oauthModel import UserDataModel, UserInsertModel, UserRegisterModel, UserUpdateModel
from ..utils import (
    hash_pass
)

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scheme_name="JWT"
)

def get_current_user(id: str, db: Database) -> UserDataModel:
    user = get_user_by_id(id, db)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return user

def register_user(user: UserRegisterModel, db: Database):
    userData = UserInsertModel(
        username=user.username,
        email= user.email,
        password= hash_pass(user.password),
        role= "user"
    )
    #validate if exist user
    user_verify = get_user_by_username(user.username.lower(), db)
    if(user_verify != None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User alredy exist"
        )

    user_data = userData.model_dump()
    try:
        result = insert_user(user_data, db)
        return {"message": "User created successfully", "user_id": str(result.inserted_id)}
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
def Update_user(id: str, user: UserUpdateModel, db: Database):
    userData = get_user_by_id(id, db)

    if(userData == None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User alredy exist"
        )

    user.username = user.username if user.username is not None else userData.username
    user.email = user.email if user.email is not None else userData.email
    user.password = hash_pass(user.password) if user.password is not None else userData.password

    userDataDic = user.model_dump()
    result = update_user(id, userDataDic, db)
    if(result.matched_count > 0): 
        return {"message": "User update successfully"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User no update"
    )

def Delte_user(id: str, db:Database):
    result = delte_user(id, db)
    if(result.deleted_count > 0): 
        return {"message": "User delete successfully"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="User no delte"
    )
