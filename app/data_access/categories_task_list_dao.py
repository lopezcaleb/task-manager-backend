from fastapi import HTTPException, status
from pymongo.database import Database
from bson import ObjectId

from app.models.categoriesTaskListModels import taskListCategoriesModel, dataTaskListCategoriesModel, taskListCategoriesModel, dataTaskListCategoriesModel

def get_all_list_task_categories_dao(user_id, db: Database) -> taskListCategoriesModel:
    try:
        cursor = db["task_list_categories"].find({"user_id": user_id}, projection={"user_id": 0})
        if cursor:
            task_list = [dataTaskListCategoriesModel(
                name=item['name'], 
                id=str(item["_id"])) for item in cursor]
            categories_task_list = taskListCategoriesModel(taskList=task_list)
            return categories_task_list
        else:
            return None
    except Exception as e:
        print(f"Error {e}")
        return Exception()
    
def get_task_list_categories_dao(id: str, db: Database) -> dataTaskListCategoriesModel:
    try: 
        result = db["task_list_categories"].find_one({"_id": ObjectId(id)})
        if result:
            categories = dataTaskListCategoriesModel(id=str(result["_id"]), name=result["name"])
            return categories
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

def insert_task_list_categories_dao(model: str, db: Database):
    try:
        result = db["task_list_categories"].insert_one(model)
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error {e}")
        return Exception()

def update_task_list_categories_dao(id: str, model: str, db: Database):
    try:
        result = db["task_list_categories"].update_one({"_id": ObjectId(id)}, {"$set": model})
        if result: 
            return result
        else: 
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def delete_task_list_categories_dao(id: str, db: Database):
    try:
        result = db["task_list_categories"].delete_one({"_id": ObjectId(id)})
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")