from fastapi import FastAPI

from api.routes import role_routes, user_routes
from database.data_initializer import initialize_data
from database.db_connection import SessionLocal, engine, Base


# Create database tables
Base.metadata.create_all(bind=engine)


def startup_event():
    db = SessionLocal()         # Create a new session instance
    try:
        initialize_data(db)     # Call the function with a valid session
    finally:
        db.close()              # Ensure the session is closed properly

startup_event()


app = FastAPI(title="UserService", version="1.0")

app.include_router(user_routes.router, prefix="/user-service", tags=["user"])

app.include_router(role_routes.router, prefix="/user-service", tags=["role"])


@app.get("/")
def read_root():
    return {"message": "User Service is running!"}