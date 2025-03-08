from sqlalchemy.orm import Session

from event import kafka_producer
from model.user import User
from schema.user_schema import UserCreate


def create_user(db: Session, user_data: UserCreate):

    user = User(firstname=user_data.firstname, lastname=user_data.lastname, email=user_data.email, password=user_data.password)

    db.add(user)
    db.commit()
    db.refresh(user)

    # Publish Kafka Event
    kafka_producer.send_event("user.registered", {"user_id": user.id, "email": user.email})

    return {"message": "Your form has been submitted successfully. After validation, you will be able to access the library."}