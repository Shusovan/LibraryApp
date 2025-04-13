import threading
from fastapi import FastAPI

from api.routes import role_routes, user_routes
from database.data_initializer import initialize_data
from database.db_connection import SessionLocal, engine, Base
from event.borrow_event import consume_kafka


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


# # Run Kafka consumer in a separate thread when the app starts
# def start_kafka_consumer():
#     kafka_thread = threading.Thread(target=consume_kafka, daemon=True)
#     kafka_thread.start()

# # Start Kafka after Uvicorn starts
# @app.on_event("startup")
# def on_startup():
#     print("🚀 AdminService has started... Initializing Kafka consumer.")
#     start_kafka_consumer()
    

@app.get("/")
def read_root():
    return {"message": "User Service is running!"}