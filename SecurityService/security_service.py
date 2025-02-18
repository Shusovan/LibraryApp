from fastapi import FastAPI

from api.routes import role_routes
from database.data_initializer_role import initialize_role
from database.db_connection import SessionLocal, engine, Base


# Create database tables
Base.metadata.create_all(bind=engine)


def startup_event():
    db = SessionLocal()       # Create a new session instance
    try:
        initialize_role(db)  # Call the function with a valid session
    finally:
        db.close()            # Ensure the session is closed properly

startup_event()


app = FastAPI(title="SecurityService", version="1.0")

app.include_router(role_routes.router, prefix="/security-service", tags=["security"])


@app.get("/")
def read_root():
    return {"message": "Security Service is running!"}