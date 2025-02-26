from pymongo.database import Database 
from bson import ObjectId
from typing import List

from app.data_access.task_dao import GetTaskByTaskListId_dao
from app.models.taskListModel import ListTaskListModel, ListTaskListModel, TaskListModel, TaskListModel, TaskToListModel
from app.models.taskModels import TaskModel

def GetAllTaskList_dao(user_id: str, db: Database) -> ListTaskListModel:
    try:
        result = db["task_list"].find({"user_id": user_id})
        if result:

            listData: List[TaskListModel] = []
            
            for item in result:
                # Get all task asociate to list
                responseTask = GetTaskByTaskListId_dao(user_id=user_id, taskList_id=str(item['_id']), db=db)
                
                listData.append(TaskListModel(
                    id=str(item['_id']),
                    name=item['name'],
                    daysActive=item['daysActive'],
                    isRecurrent=item['isRecurrent'],
                    lastActive=item['lastActive'],
                    details=item['details'],
                    taskListCategory_id=item['taskListCategory_id'],
                    user_id=item['user_id'],
                    state=item['state'],
                    task=[TaskModel(
                        id=itemTask.id,
                        categorieTask_id=itemTask.categorieTask_id,
                        details=itemTask.details,
                        name=itemTask.name,
                        taskList_id=itemTask.taskList_id,
                        user_id=itemTask.user_id
                    ) for itemTask in responseTask.tasks]
                ))

            taskList = ListTaskListModel(task_lists=listData)
            return taskList
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def GetTaskList_dao(id: str, user_id: str,db: Database) -> TaskListModel:
    try:
        result = db["task_list"].find_one({"_id": ObjectId(id), "user_id": user_id})
        if result:
            # Get all task asociate to list
            responseTask = GetTaskByTaskListId_dao(user_id=user_id, taskList_id=str(result['_id']), db=db)

            taskList = TaskListModel(
                id=str(result['_id']),
                name=result['name'],
                daysActive=result['daysActive'],
                isRecurrent=result['isRecurrent'],
                lastActive=result['lastActive'],
                user_id=result['user_id'],
                details=result['details'],
                taskListCategory_id=result['taskListCategory_id'],
                state=result['state'],
                task=[TaskModel(
                    id=itemTask.id,
                    categorieTask_id=itemTask.categorieTask_id,
                    details=itemTask.details,
                    name=itemTask.name,
                    taskList_id=itemTask.taskList_id,
                    user_id=itemTask.user_id
                ) for itemTask in responseTask.tasks]
             )
            return taskList
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def InsertTaskList_dao(model: str, db: Database):
    try:
        result = db["task_list"].insert_one(model)
        if result:
            return result
        else:
            None
    except Exception as e:
        print(f"Error: {e}")

def UpdateTaskList_dao(id: str, model: str, db: Database):
    try:
        result = db['task_list'].update_one({"_id": ObjectId(id)}, {"$set": model})
        if result:
            return result
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    
def DeleteTaskList_dao(id: str, user_id: str, db: Database):
    try:
        result = db['task_list'].delete_one({"_id": ObjectId(id), "user_id": user_id})
        if result: 
            return result
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    
def GetTaskToTaskList(id: str, user_id: str, db: Database) -> TaskToListModel:
    try:
        result = db['task'].find({"taskList_id": id, "user_id": user_id})
        if result:
            taskList = [TaskModel(
                id=str(item["_id"]),
                name=item["name"],
                details=item["details"],
                categorieTask_id=item["categorieTask_id"],
                taskList_id=item["taskList_id"],
                user_id=item["user_id"]
            ) for item in result]
            return TaskToListModel(id=id, tasks=taskList)
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return Exception()
    