from fastapi import HTTPException, status
from pymongo.database import Database
from app.data_access.categories_task_list_dao import delete_task_list_categories_dao, get_all_list_task_categories_dao, get_task_list_categories_dao, insert_task_list_categories_dao, update_task_list_categories_dao
from app.models.categoriesTaskListModels import taskListCategoriesAllModel, taskListCategoriesModel, taskListCategoriesModel, dataTaskListCategoriesModel, taskListCategoriesRegisterModel, taskListCategoriesUpdateModel
from app.utils import validate_formad_id


def get_all_list_task_categories(user_id: id, db: Database) -> taskListCategoriesModel:
    taskList = get_all_list_task_categories_dao(user_id, db)
    if taskList == None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error to get task list"
        )
    return taskList

def get_task_list_categories(id: str, db: Database) -> dataTaskListCategoriesModel:
    try:
        validate = validate_formad_id(id)
        if not validate:
            raise HTTPException(
                status_code=400,
                detail="The id format not is valid"
            )
        categories = get_task_list_categories_dao(id, db)
        if categories == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task list not found"
            )
        return categories
    except Exception as e:
        if isinstance(e, HTTPException):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
        else:
            Exception()

def insert_categorie_task_list(model: taskListCategoriesRegisterModel, user_id: str, db: Database ):
    modelData = taskListCategoriesAllModel(
        name = model.name, 
        user_id = user_id
        )

    modelDump = modelData.model_dump()
    result = insert_task_list_categories_dao(modelDump, db)
    if result == None:
        raise Exception()
    return result

def update_categories_task_list(id: str, model: taskListCategoriesUpdateModel, db:Database):
    data = model.model_dump()
    result = update_task_list_categories_dao(id, data, db)
    if result == None:
        raise Exception()
    if(result.matched_count <= 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task list no exist"
        )
    return result

def delete_categories_task_list(id: str, db: Database):
    result = delete_task_list_categories_dao(id, db)
    if result == None:
        raise Exception()
    if result.deleted_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="task list not found"
        )
    return result