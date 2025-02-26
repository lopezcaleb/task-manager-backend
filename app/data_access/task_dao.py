from bson import ObjectId
from pymongo.database import Database

from app.models.taskModels import TaskListModel, TaskModel

def GetAllTask_dao(user_id: str, db: Database) -> TaskListModel:
    try:
        result = db["task"].find({"user_id": user_id})
        if result:
            taskList = [TaskModel(
                id=str(item["_id"]),
                name=item["name"],
                details=item["details"],
                categorieTask_id=item["categorieTask_id"],
                taskList_id=item["taskList_id"],
                user_id=item["user_id"]
            ) for item in result]
            listData = TaskListModel(tasks=taskList)
            return listData
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    
def GetTask_dao(id: str, user_id: str, db: Database) -> TaskModel:
    try:
        result = db["task"].find_one({"_id": ObjectId(id), "user_id": user_id})
        if result:
            return TaskModel( 
                id=str(result["_id"]),
                name=result["name"],
                details=result["details"],
                categorieTask_id=result["categorieTask_id"],
                taskList_id=result["taskList_id"],
                user_id=result["user_id"]
            )
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    
def InsertTask_dao(model: str, db: Database):
    try:
        result = db["task"].insert_one(model)
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    
def UpdateTask_dao(id: str, user_id: str, model: str, db:Database):
    try:
        result = db["task"].update_one({"_id": ObjectId(id), "user_id": user_id}, {"$set": model})
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    
def DeleteTask_dao(id: str, user_id: str, db:Database):
    try:
        result = db["task"].delete_one({"_id": ObjectId(id), "user_id": user_id})
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    
def GetTaskByTaskListId_dao(user_id: str, taskList_id:str, db: Database) -> TaskListModel:
    try:
        result = db["task"].find({"user_id": user_id, "taskList_id": taskList_id})
        if result:
            taskList = [TaskModel(
                id=str(item["_id"]),
                name=item["name"],
                details=item["details"],
                categorieTask_id=item["categorieTask_id"],
                taskList_id=item["taskList_id"],
                user_id=item["user_id"]
            ) for item in result]
            listData = TaskListModel(tasks=taskList)
            return listData
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()