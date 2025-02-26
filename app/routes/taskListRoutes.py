from fastapi import APIRouter, Depends, HTTPException, Response, status
from pymongo.database import Database
from app.database import get_db
from app.models.oauthModel import TokenPayload
from app.models.taskListModel import RequestTaskListInsertModel, RequestTaskListUpdateModel
from app.services.taskListServices import delete_task_list, get_all_task_list, get_task_list, get_task_to_task_list, insert_task_list, update_task_list
from app.utils import verify_auth

routesTaskList = APIRouter()
db = get_db()

@routesTaskList.get('/all', summary="get all task list", tags=["task list"], status_code=status.HTTP_200_OK)
def GetAll(tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        taskList = get_all_task_list(tokenData.sub, db)
        return taskList
    except Exception as e:
        if isinstance(e, HTTPException):
            return Response(status_code=e.status_code, content=e.detail)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
        
@routesTaskList.post('/', summary="Insert new task list", tags=["task list"], status_code=status.HTTP_201_CREATED)
def Create(model: RequestTaskListInsertModel, tokenData: TokenPayload = Depends(verify_auth),db: Database = Depends(get_db)):
    try:
        result = insert_task_list(tokenData.sub, model, db)
        return {"message": "task list created successfully", "task_list_id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(status_code=e.status_code, content=e.detail)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")

@routesTaskList.get('/', summary="Get task list by id", tags=["task list"], status_code=status.HTTP_200_OK)
def Get(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        result = get_task_list(id, tokenData.sub, db)
        return result
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(status_code=e.status_code, content=e.detail)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
        
@routesTaskList.put('/', summary="Insert new task list", tags=["task list"], status_code=status.HTTP_200_OK)
def Update(id: str, model: RequestTaskListUpdateModel, tokenData: TokenPayload = Depends(verify_auth),db: Database = Depends(get_db)):
    try:
        update_task_list(id, tokenData.sub, model, db)
        return {"message": "task list update successfully"}
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(status_code=e.status_code, content=e.detail)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
        
@routesTaskList.delete("/", summary="Delete task list by id", tags=[""], status_code=status.HTTP_200_OK)
def Delete(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        delete_task_list(id, tokenData.sub, db)
        return {"message": "task list delete successfully"}
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(status_code=e.status_code, content=e.detail)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")
        
@routesTaskList.get('/task', summary="Get task to list task", tags=["task list"], status_code=status.HTTP_200_OK)
def GetTaskToListTask(id: str, tokenData: TokenPayload = Depends(verify_auth), db: Database = Depends(get_db)):
    try:
        result = get_task_to_task_list(id=id, user_id=tokenData.sub, db=db)
        return result
    except Exception as e:
        print(f"Error: {e}")
        if isinstance(e, HTTPException):
            return Response(status_code=e.status_code, content=e.detail)
        else:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal server error")