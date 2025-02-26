from pydantic import BaseModel


class CategoriesTaskModel(BaseModel):
    id: str
    name: str

class CategoriesTaskDataModel(BaseModel):
    name: str
    user_id: str

class CategoriesTaskDataRequestModel(BaseModel):
    name: str

class CategoriesTaskListModel(BaseModel):
    categoriesTasks: list[CategoriesTaskModel]

