from fastapi import FastAPI

from api.routes import book_routes
from database.db_connection import engine, Base


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="BookService", version="1.0")

app.include_router(book_routes.router, prefix="/book-service", tags=["book"])


@app.get("/")
def read_root():
    return {"message": "Book Service is running!"}