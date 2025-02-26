from pymongo.database import Database
from bson import ObjectId

from app.models.categoriesTaskModel import CategoriesTaskListModel, CategoriesTaskModel 

def GetAllCategoriesTask_dao(user_id: str, db: Database) -> CategoriesTaskListModel:
    try:
        result = db['categories_task'].find({"user_id": user_id})
        if result:
            taskList = [CategoriesTaskModel(id=str(item["_id"]),name=item["name"]) for item in result]
            return CategoriesTaskListModel(categoriesTasks=taskList)
        else:
            return None
    except Exception as e:
        print(f"ErroR: {e}")
        return Exception()

def GetCategoriesTask_dao(id: str, user_id: str, db: Database) -> CategoriesTaskModel:
    try:
        result = db['categories_task'].find_one({"_id": ObjectId(id), "user_id": user_id})
        if result:
            return CategoriesTaskModel(id=str(result["_id"]), name=result["name"])
        else:
            return None
    except Exception as e:
        print(f"ErroR: {e}")
        return Exception()

def InsertCategoriesTask_dao(model: str, db: Database):
    try:
        result = db['categories_task'].insert_one(model)
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"ErroR: {e}")
        return Exception()
    
def UpdateCategoriesTask_dao(id: str, model:str ,db: Database):
    try:
        result = db['categories_task'].update_one({"_id": ObjectId(id)}, {"$set": model})
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"ErroR: {e}")
        return Exception()
    
def DeleteCategoriesTask_dao(id: str, user_id:str, db: Database):
    try:
        result = db['categories_task'].delete_one({"_id": ObjectId(id), "user_id": user_id})
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"ErroR: {e}")
        return Exception()