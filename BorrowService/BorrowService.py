from fastapi import FastAPI

from core.db_connection import Base, engine
from routes import borrow_routes


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="BookService", version="1.0")

app.include_router(borrow_routes.router, prefix="/borrow-service", tags=["book"])


@app.get("/")
def read_root():
    return {"message": "Borrow Service is running!"}