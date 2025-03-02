from fastapi import FastAPI

from api.routes import auth_routes, user_routes
from database.db_connection import SessionLocal, engine, Base


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="SecurityService", version="1.0")

app.include_router(user_routes.router, prefix="/security-service", tags=["security"])

app.include_router(auth_routes.router, prefix="/security-service", tags=["security"])


@app.get("/")
def read_root():
    return {"message": "Security Service is running!"}