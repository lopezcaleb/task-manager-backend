from fastapi import HTTPException, status
from pymongo.database import Database

from app.data_access.categories_task_dao import DeleteCategoriesTask_dao, GetAllCategoriesTask_dao, GetCategoriesTask_dao, InsertCategoriesTask_dao, UpdateCategoriesTask_dao
from app.models.categoriesTaskModel import CategoriesTaskDataModel, CategoriesTaskDataRequestModel, CategoriesTaskListModel, CategoriesTaskModel 

def GetAllCategoriesTask(user_id: str, db: Database) -> CategoriesTaskListModel:
    result = GetAllCategoriesTask_dao(user_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="categories task not found"
        )
    return result

def GetCategoriesTask(id: str, user_id: str, db: Database) -> CategoriesTaskModel:
    result = GetCategoriesTask_dao(id, user_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="categories task not found"
        )
    return result

def InsertCategoriesTask(user_id: str, model: CategoriesTaskDataRequestModel, db: Database):
    categorieTask = CategoriesTaskDataModel(name=model.name, user_id=user_id)
    result = InsertCategoriesTask_dao(categorieTask.model_dump(), db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="task categories was not register"
        )
    return result

def UpdateCategoriesTask(id: str, user_id: str, model: CategoriesTaskDataRequestModel, db: Database):
    categorieTask = GetCategoriesTask_dao(id, user_id, db)
    if categorieTask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="categories task not found"
        )
    
    model.name = model.name if model.name is not None else categorieTask.name

    result = UpdateCategoriesTask_dao(id, model.model_dump(), db)

    if result is None or result.matched_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="task categories was not update"
        )
    
    return result

def DeleteCategoriesTask(id: str,user_id: str, db: Database):
    result = DeleteCategoriesTask_dao(id, user_id, db)
    if result is None or result.deleted_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="task categories not found"
        )
    return result