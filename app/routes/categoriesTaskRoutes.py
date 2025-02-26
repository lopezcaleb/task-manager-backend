from fastapi import APIRouter, Depends, HTTPException, Response, status
from pymongo.database import Database

from app.database import get_db
from app.models.categoriesTaskModel import CategoriesTaskDataRequestModel
from app.services.categoriesTaskServices import DeleteCategoriesTask, GetAllCategoriesTask, GetCategoriesTask, InsertCategoriesTask, UpdateCategoriesTask
from app.utils import verify_auth
from ..models.oauthModel import TokenPayload

routerCategoriesTask = APIRouter()
db = get_db()

@routerCategoriesTask.get('/all', summary="Get all categoires task", tags=["categories_task"], status_code=status.HTTP_200_OK)
def GetAll(tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        return GetAllCategoriesTask(tokenData.sub, db)
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code, content=e.detail
            )
        else:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Intenal server error"
            )

@routerCategoriesTask.get('/', summary="Get task categorie by id", tags=["categories_task"], status_code=status.HTTP_200_OK)
def Get(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        return GetCategoriesTask(id, tokenData.sub, db)
    except Exception as e:
        print(f"Error: {e}")

        if isinstance(e, HTTPException):

            return Response(
                status_code=e.status_code, content=e.detail
            )
        else:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Intenal server error"
            )

@routerCategoriesTask.post('/', summary="Get task categorie by id", tags=["categories_task"], status_code=status.HTTP_201_CREATED)
def Create(model: CategoriesTaskDataRequestModel, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        result = InsertCategoriesTask(tokenData.sub, model, db)
        return {"message": "task list created successfully", "task_list_id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code, content=e.detail
            )
        else:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Intenal server error"
            )

@routerCategoriesTask.put('/', summary="Get task categorie by id", tags=["categories_task"], status_code=status.HTTP_200_OK)
def Update(id: str, model: CategoriesTaskDataRequestModel, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        UpdateCategoriesTask(id, tokenData.sub ,model, db)
        return {"msg": "task categories was update"}
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code, content=e.detail
            )
        else:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Intenal server error"
            )

@routerCategoriesTask.delete('/', summary="Get task categorie by id", tags=["categories_task"], status_code=status.HTTP_200_OK)
def Delete(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        DeleteCategoriesTask(id, tokenData.sub, db)
        return {"msg": "task categories was delete"}
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code, content=e.detail
            )
        else:
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Intenal server error"
            )