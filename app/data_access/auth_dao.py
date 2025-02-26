from app.database import get_db
from pymongo.database import Database

from app.models.oauthModel import UserModel

def auth_user(username: str, db: Database) -> UserModel:
    try:
        user_data  = db["users"].find_one({"username": username})
        if user_data:
            user_data['id'] = str(user_data['_id'])
            user = UserModel(**user_data)
            return user
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
   