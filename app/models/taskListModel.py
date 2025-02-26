from enum import Enum
from typing import Optional
from pydantic import BaseModel

from app.models.taskModels import TaskModel


class DaysOfWeek(str, Enum):
    Sunday = "Sunday"
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"

class RequestTaskListInsertModel(BaseModel):
    name: str
    daysActive: Optional[list[DaysOfWeek]] = None
    isRecurrent: Optional[bool]
    details: str
    taskListCategory_id: str

class TaskListInsertModel(BaseModel):
    name: str
    daysActive: Optional[list[DaysOfWeek]] = None
    isRecurrent: Optional[bool] = False
    lastActive: str
    user_id: str
    details: str
    taskListCategory_id: str
    state: str

class RequestTaskListUpdateModel(BaseModel):
    name: Optional[str]
    daysActive: Optional[list[DaysOfWeek]] = None
    isRecurrent: Optional[bool]
    details: Optional[str]
    taskListCategory_id: Optional[str]

class TaskListUpdateModel(BaseModel):
    name: Optional[str]
    daysActive: Optional[list[DaysOfWeek]] = None
    isRecurrent: Optional[bool] = False
    lastActive: Optional[str]
    details: Optional[str]
    taskListCategory_id: Optional[str]
    state: Optional[str]

class TaskListModel(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    daysActive: Optional[list[DaysOfWeek]] = None
    isRecurrent: Optional[bool] = None
    lastActive: Optional[str] = None
    user_id: Optional[str] = None
    details: Optional[str] = None
    taskListCategory_id: Optional[str] = None
    state: Optional[str] = None
    task: Optional[list[TaskModel]] = None

class ListTaskListModel(BaseModel):
    task_lists: list[TaskListModel]

class TaskToListModel(BaseModel):
    id: str
    tasks: list[TaskModel]