from fastapi import FastAPI

from api.routes import user_routes
from database.db_connection import engine, Base


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="UserService", version="1.0")

app.include_router(user_routes.router, prefix="/user-service", tags=["user"])


@app.get("/")
def read_root():
    return {"message": "User Service is running!"}