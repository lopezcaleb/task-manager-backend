import datetime
from fastapi import HTTPException, status
from pymongo.database import Database

from app.data_access.task_list_dao import DeleteTaskList_dao, GetAllTaskList_dao, GetTaskList_dao, GetTaskToTaskList, InsertTaskList_dao, UpdateTaskList_dao
from app.models.taskListModel import DaysOfWeek, ListTaskListModel, RequestTaskListInsertModel, RequestTaskListUpdateModel, TaskListInsertModel, TaskListModel, TaskListUpdateModel, TaskToListModel
from app.services.categoriesTaskListServices import get_task_list_categories
from app.utils import validate_formad_id

def get_all_task_list(user_id: str, db: Database) -> ListTaskListModel:
    taskList = GetAllTaskList_dao(user_id, db)
    if taskList == None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error to get all task list"
        )
    return taskList

def insert_task_list(user_id: str, model: RequestTaskListInsertModel, db: Database):
    validate = validate_formad_id(model.taskListCategory_id)
    if not validate:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Param taskListCategory_id is not valid Id"
            )
    try: 
        result = get_task_list_categories(model.taskListCategory_id, db)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="category not found"
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )
        else:
            return Exception()

    lastActive = get_last_date_task_list_active(model.daysActive)
    state = "create"

    # Obtener fecha actual
    hoy = datetime.datetime.today()
    # Obtener el nombre del día de la semana
    today = hoy.strftime("%A")

    listOrder = sort_list_of_days_of_the_week(model.daysActive)
    if listOrder[0].value == today:
        state = "active"

    # delete nameDay to daysActive if is active and if no is recurrent----------------


    taskList = TaskListInsertModel(
        name = model.name,
        daysActive=model.daysActive,
        isRecurrent= model.isRecurrent,
        lastActive= str(lastActive),
        user_id= user_id,
        details= model.details,
        taskListCategory_id= model.taskListCategory_id,
        state= state
    )
    
    result = InsertTaskList_dao(taskList.model_dump(), db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in data base"
        )
    return result

def get_task_list(id: str,user_id: str, db: Database) -> TaskListModel:
    try:
        result = GetTaskList_dao(id, user_id ,db)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task list not foud"
            )

        return result
    except Exception as e:
        print(f"Error: {e}")
        return Exception()

def update_task_list(id: str, user_id: str,model: RequestTaskListUpdateModel,db: Database):
    if model.taskListCategory_id is not None:
        validate = validate_formad_id(model.taskListCategory_id)
        if not validate:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Param taskListCategory_id is not valid Id"
                )
        
    getTaskList= GetTaskList_dao(id, user_id, db)

    if getTaskList is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task list not foud"
        )

    taskList = TaskListUpdateModel(
        name=model.name if model.name is not None else getTaskList.name,
        daysActive=model.daysActive if model.daysActive is not None else getTaskList.daysActive,
        isRecurrent=model.isRecurrent if model.isRecurrent is not None else getTaskList.isRecurrent,
        taskListCategory_id=model.taskListCategory_id if model.taskListCategory_id is not None else getTaskList.taskListCategory_id,
        details=model.details if model.details is not None else getTaskList.details,
        lastActive=getTaskList.lastActive,
        state=getTaskList.state
    )

    # Validar taskList.lastActive -------------------------------------------
    if model.daysActive is not None:
        lastActive = str(get_last_date_task_list_active(model.daysActive))
        taskList.lastActive = lastActive
        hoy = datetime.datetime.today()
        # Obtener el nombre del día de la semana
        today = hoy.strftime("%A")

        listOrder = sort_list_of_days_of_the_week(model.daysActive)
        if listOrder[0].value == today:
            taskList.state = "active"

    taskList_dump = taskList.model_dump()
    result = UpdateTaskList_dao(id, taskList_dump, db)

    if result is None or result.matched_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task list not foud"
        )
    
    return result

def delete_task_list(id: str, user_id: str, db: Database):
    result = DeleteTaskList_dao(id, user_id, db)
    if result is None or result.deleted_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task list not found"
        )
    return result

def get_task_to_task_list(id: str, user_id: str, db: Database) -> TaskToListModel:
    # validate id format 
    if validate_formad_id(id) is not True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task list id is not valid"
        )
    
    # validate if exist task list
    listTask = GetTaskList_dao(id, user_id ,db)
    if listTask is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    
    result = GetTaskToTaskList(id, user_id, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task list not found"
        )
    return result
    
# logic methods
def get_last_date_task_list_active(model: list[DaysOfWeek]) -> datetime:
    # Obtener fecha actual dia actual
    today = datetime.datetime.today()

    # Si la lista esta vacia agregarle el dia actual
    if not model:
        lastActive = today.date()
        return lastActive

    # Ordenar los dias de la semana en la lista
    sorted_days = sort_list_of_days_of_the_week(model)

    # Siguiente dia en que la tarea estara activa
    dayName = sorted_days[0].value

    # Obtener la fecha en que la tarea estara activa
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        nameOtherDay = day.strftime("%A")
        if nameOtherDay == dayName:
            lastActive = day.date()
            return lastActive
        
def sort_list_of_days_of_the_week(model: list[DaysOfWeek]) -> list[DaysOfWeek]:
    # Crear un diccionario para mapear cada día a su índice en la enumeración
    days_index = {day: index for index, day in enumerate(DaysOfWeek)}

    # Ordenar la lista usando el índice del día en la enumeración
    sorted_days = sorted(model, key=lambda day: days_index[day])
    return sorted_days

