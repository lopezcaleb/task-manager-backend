from pydantic import BaseModel


class TaskModel(BaseModel):
    id: str
    name: str
    details: str
    categorieTask_id: str
    taskList_id: str
    user_id: str

class TaskDataModel(BaseModel):
    name: str
    details: str
    categorieTask_id: str
    taskList_id: str
    user_id: str

class TaskRequestModel(BaseModel):
    name: str
    details: str
    categorieTask_id: str
    taskList_id: str

class TaskListModel(BaseModel):
    tasks: list[TaskModel]