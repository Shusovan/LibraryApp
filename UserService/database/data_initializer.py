from sqlalchemy.orm import session

from model.role import Role


# pre-populate SUPER_ADMIN to database
def initialize_data(db : session):

    roles = ["USER", "GUEST"]

    super_admin_id = None

    for role_name in roles:
        
        # Check if the role already exists
        existing_role = db.query(Role).filter_by(name=role_name).first()
        
        # If the role doesn't exist, create it
        if not existing_role:
            new_role = Role(name=role_name)
            
            db.add(new_role)
            db.commit()                             # Commit the transaction to persist the role
            db.refresh(new_role)   