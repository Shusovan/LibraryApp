from sqlalchemy.orm import Session
from models.role import Role

def initialize_role(db: Session):
    
    roles = ["SUPER_ADMIN", "ADMIN", "LIBRARIAN"]
    
    for role_name in roles:
        existing_role = db.query(Role).filter_by(name=role_name).first()
        
        if not existing_role:
            db.add(Role(name=role_name))

    db.commit()
