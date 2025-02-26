from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.database import get_db
from pymongo.database import Database

from app.models.oauthModel import TokenPayload
from app.models.categoriesTaskListModels import taskListCategoriesModel, dataTaskListCategoriesModel, taskListCategoriesRegisterModel, taskListCategoriesUpdateModel
from app.services.categoriesTaskListServices import delete_categories_task_list, get_all_list_task_categories, get_task_list_categories, insert_categorie_task_list, update_categories_task_list
from app.utils import verify_auth, verify_rol

routerRoutesTaskList = APIRouter()
db = get_db()

@routerRoutesTaskList.get('/all', summary="Get all task list", tags=["categories task api"], status_code=status.HTTP_200_OK, response_model=taskListCategoriesModel)
def get_all(tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    verify_rol(["admin", "user"], tokenData.role)
    try:
        taskList = get_all_list_task_categories(tokenData.sub, db)
        return taskList
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
        
@routerRoutesTaskList.get('/', summary="get task list", tags=["categories task api"], status_code=status.HTTP_200_OK)
def get(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    verify_rol(["admin", "user"], tokenData.role)
    try:
        categories = get_task_list_categories(id, db)
        return categories
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")

@routerRoutesTaskList.post('/', summary="Create new task list", tags=["categories task api"], status_code=status.HTTP_201_CREATED)
def create(model: taskListCategoriesRegisterModel, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    verify_rol(["admin", "user"], tokenData.role)
    try:
        result = insert_categorie_task_list(model, tokenData.sub, db)
        return {"message": "task list created successfully", "task_list_id": str(result.inserted_id)}
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
        
@routerRoutesTaskList.put('/', summary="Update task list", tags=["categories task api"], status_code=status.HTTP_200_OK)
def update(id: str, model: taskListCategoriesUpdateModel, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    verify_rol(["admin", "user"], tokenData.role)
    try:
        update_categories_task_list(id, model, db)
        return {"msg": "task list was update"}
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")

@routerRoutesTaskList.delete('/', summary="Delete task list", tags=["categories task api"], status_code=status.HTTP_200_OK)
def delete(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    verify_rol(["admin", "user"], tokenData.role)
    try:
        delete_categories_task_list(id, db)
        return {"msg": "task list was delete"}
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(content=e.detail, status_code=e.status_code)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
