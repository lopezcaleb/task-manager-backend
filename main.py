from fastapi import FastAPI
from app.routes.oauthRoutes import routerOauth
from app.routes.userRoutes import routerUser
from app.routes.categoriesTaskListRoutes import routerRoutesTaskList
from app.routes.taskListRoutes import routesTaskList
from app.routes.categoriesTaskRoutes import routerCategoriesTask
from app.routes.taskRoutes import routesTask
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar CORS para permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(routerOauth, prefix="/api/auth")
app.include_router(routerUser, prefix="/api/user")
app.include_router(routerRoutesTaskList, prefix="/api/categories/tasklist")
app.include_router(routesTaskList, prefix="/api/tasklist")
app.include_router(routerCategoriesTask, prefix="/api/categories/task")
app.include_router(routesTask, prefix="/api/task")

@app.get("/")
async def root():
    return { "message": "Hello World" }
