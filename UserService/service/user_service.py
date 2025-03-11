from fastapi import HTTPException
from sqlalchemy.orm import Session

from event import kafka_producer
from model.role import Role
from model.user import User
from schema.user_schema import ApproveUserRequest, UserCreate
from security.encrypt import hash_password


def create_user(db: Session, user_data: UserCreate):

    encypted_password = hash_password(user_data.password)

    user_role = db.query(Role).filter(Role.name == "USER").first()

    user = User(firstname=user_data.firstname, lastname=user_data.lastname, email=user_data.email, password=encypted_password, role=user_role)

    db.add(user)
    db.commit()
    db.refresh(user)

    # Publish Kafka Event
    kafka_producer.send_event("user.registered", {"user_id": user.id, "email": user.email})

    return {"message": "Your form has been submitted successfully. After validation, you will be able to access the library."}


def user_approved(email: str, user_data: dict, db: Session):

    # db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.user_id = user_data["user_id"]
    user.status = user_data["status"]
    user.verified_by = user_data["verified_by"]
    
    db.commit()
    db.refresh(user)

    return {f"message": "User approved successfully", "user_id": user.user_id}