from sqlalchemy.orm import Session
from models.admin import Admin
from schemas.admin_schema import AdminCreate
from security.encrypt import hash_password


def create_admin(db: Session, admin_data: AdminCreate):
    
    hashed_password = hash_password(admin_data.password)
    
    db_admin = Admin(name=admin_data.name, email=admin_data.email, password=hashed_password)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    
    return db_admin


def get_all_admins(db: Session):
    return db.query(Admin).all()


def get_admin_by_email(db: Session, email: str):

    return db.query(Admin).filter(Admin.email == email).first()