from pymongo import MongoClient

# Configuración de la base de datos
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "task-manager"

def get_db():
    client = MongoClient(MONGO_URI)
    try:
        db = client[DATABASE_NAME]
        yield db
    finally:
        client.close()