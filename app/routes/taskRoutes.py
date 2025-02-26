from fastapi import APIRouter, Depends, Response, status, HTTPException
from pymongo.database import Database

from app.database import get_db
from app.models.taskModels import TaskRequestModel
from app.services.taskServices import DeleteTask, GetAllTask, GetTask, InsertTask, UpdateTask

from ..models.oauthModel import TokenPayload
from ..utils import verify_auth

routesTask = APIRouter()

@routesTask.get('/all', summary="Get all task", tags=["task"], status_code=status.HTTP_200_OK)
def GetAll(tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        return GetAllTask(user_id=tokenData.sub, db=db)
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code,
                content=e.detail
            )
        else:
            Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal server error"
            )

@routesTask.get('/', summary="Get task by id", tags=["task"], status_code=status.HTTP_200_OK)
def Get(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        return GetTask(id=id, user_id=tokenData.sub, db=db)
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code,
                content=e.detail
            )
        else:
            Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal server error"
            )

@routesTask.post('/', summary="Insert new task", tags=["task"], status_code=status.HTTP_201_CREATED)
def Insert(model: TaskRequestModel, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        result = InsertTask(user_id=tokenData.sub, model=model, db=db)
        return {"message": "task created successfully", "task_id": str(result.inserted_id)}
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code,
                content=e.detail
            )
        else:
            Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal server error"
            )

@routesTask.put('/', summary="Update task", tags=["task"], status_code=status.HTTP_200_OK)
def Update(id: str, model: TaskRequestModel, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        UpdateTask(id=id, user_id=tokenData.sub, model=model, db=db)
        return {"message": "task update successfully"}
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code,
                content=e.detail
            )
        else:
            Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal server error"
            )

@routesTask.delete('/', summary="Delete task", tags=["task"], status_code=status.HTTP_200_OK)
def Delete(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        DeleteTask(id=id, user_id=tokenData.sub, db=db)
        return {"message": "task delete successfully"}
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(
                status_code=e.status_code,
                content=e.detail
            )
        else:
            Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content="Internal server error"
            )