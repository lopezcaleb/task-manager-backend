from pymongo.database import Database
from bson import ObjectId

from app.models.oauthModel import UserAllDataModel, UserDataModel

def get_user_by_username(username: str, db: Database) -> UserDataModel:
    try:
        user = db["users"].find_one({"username": username}, projection={"_id": 0, "password": 0})
        if(user):
            userData = UserDataModel(**user)
            return userData
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def get_user_by_id(id: str, db: Database) -> UserAllDataModel:
    try:
        user = db["users"].find_one({"_id": ObjectId(id)}, projection={"_id": 0})
        if(user):
            userData = UserAllDataModel(**user)
            return userData
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def insert_user(user_data: str, db: Database ):
    try:
        return db["users"].insert_one(user_data)
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def update_user(id:str, user_data: str, db: Database ):
    try:
        return db["users"].update_one({"_id": ObjectId(id)}, {"$set": user_data})
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def delte_user(id: str, db: Database):
    try:
        return db["users"].delete_one({"_id": ObjectId(id)})
    except Exception as e:
        print(f"Error: {e}")
        return Exception()