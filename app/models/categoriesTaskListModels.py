from pydantic import BaseModel

class taskListCategoriesAllModel(BaseModel):
    name: str
    user_id: str

class dataTaskListCategoriesModel(BaseModel):
    id: str
    name: str

class taskListCategoriesUpdateModel(BaseModel):
    name: str

class taskListCategoriesModel(BaseModel):
    taskList: list[dataTaskListCategoriesModel]

class taskListCategoriesRegisterModel(BaseModel):
    name: str