from fastapi import HTTPException, status
from pymongo.database import Database

from app.data_access.categories_task_dao import GetCategoriesTask_dao
from app.data_access.task_dao import DeleteTask_dao, GetAllTask_dao, GetTask_dao, InsertTask_dao, UpdateTask_dao
from app.data_access.task_list_dao import GetTaskList_dao
from app.models.taskModels import TaskDataModel, TaskListModel, TaskRequestModel
from app.utils import validate_formad_id

def GetAllTask(user_id: str, db: Database) -> TaskListModel:
    result = GetAllTask_dao(user_id=user_id, db=db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks not found"
        )
    return result

def GetTask(id: str, user_id: str, db: Database) -> TaskListModel:
    result = GetTask_dao(id=id, user_id=user_id, db=db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return result

def InsertTask(user_id: str, model: TaskRequestModel, db: Database) -> TaskListModel:
    # Validate format taskList_id and exist taskList_id
    if(validate_formad_id(model.taskList_id) is not True or GetTaskList_dao(id=model.taskList_id, user_id=user_id, db=db) is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="task list not found"
        )
    
    # Validate format categorieTask_id and exist categorieTask_id
    if(validate_formad_id(model.categorieTask_id) is not True or GetCategoriesTask_dao(id=model.categorieTask_id, user_id=user_id, db=db) is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="categorie task is not found"
        )

    taskModel = TaskDataModel(
        name=model.name,
        details=model.details,
        categorieTask_id=model.categorieTask_id,
        taskList_id=model.taskList_id,
        user_id=user_id,
    )
    result = InsertTask_dao(model=taskModel.model_dump() , db=db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task was not register"
        )
    return result

def UpdateTask(id: str, user_id: str, model: TaskRequestModel, db: Database) -> TaskListModel:
    if model.taskList_id is not None:
        if(validate_formad_id(model.taskList_id) is not True or GetTaskList_dao(id=model.taskList_id, user_id=user_id, db=db) is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="task list not found"
            )
    if model.categorieTask_id is not None:
        if(validate_formad_id(model.categorieTask_id) is not True or GetCategoriesTask_dao(id=model.categorieTask_id, user_id=user_id, db=db) is None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="categorie task is not found"
            )

    getTask = GetTask_dao(id=id, user_id=user_id, db=db)
    if getTask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    taskModel = TaskDataModel(
        name=model.name if getTask.name is None else model.name,
        details=model.details if getTask.details is None else model.details,
        categorieTask_id=model.categorieTask_id if getTask.categorieTask_id is None else model.categorieTask_id,
        taskList_id=model.taskList_id if getTask.taskList_id is None else model.taskList_id,
        user_id=getTask.user_id
    )
    result = UpdateTask_dao(id=id, user_id=user_id, model=taskModel.model_dump(), db=db)

    if result is None or result.matched_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task was not update"
        )
    return result

def DeleteTask(id: str, user_id: str, db: Database):
    result = DeleteTask_dao(id=id, user_id=user_id, db=db)
    if result is None or result.deleted_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks not found"
        )
    return result