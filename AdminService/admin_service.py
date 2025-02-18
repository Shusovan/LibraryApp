from fastapi import FastAPI
import uvicorn
from api.routes import admin_routes
from database.data_initializer_admin import initialize_admin
from database.db_connection import SessionLocal, engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)
from dotenv import load_dotenv

load_dotenv()


def startup_event():
    db = SessionLocal()       # Create a new session instance
    try:
        initialize_admin(db)  # Call the function with a valid session
    finally:
        db.close()            # Ensure the session is closed properly

startup_event()


app = FastAPI(title="AdminService", version="1.0")

app.include_router(admin_routes.router, prefix="/admin-service", tags=["admin"])

@app.get("/")
def read_root():
    return {"message": "Admin Service is running!"}

if __name__ == "__main__":
    uvicorn.run("admin_service:app", host="0.0.0.0", port=8001, reload=True)