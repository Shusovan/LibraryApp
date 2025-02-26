import email
from sqlalchemy.orm import session

from models.admin import Admin
from models.role import Role
from security.encrypt import hash_password


# pre-populate SUPER_ADMIN to database
def initialize_data(db : session):

    roles = ["SUPER_ADMIN", "ADMIN", "LIBRARIAN"]

    super_admin_id = None

    for role_name in roles:
        
        # Check if the role already exists
        existing_role = db.query(Role).filter_by(name=role_name).first()
        
        # If the role doesn't exist, create it
        if not existing_role:
            new_role = Role(name=role_name)
            
            db.add(new_role)
            db.commit()                             # Commit the transaction to persist the role
            db.refresh(new_role)                    # Refresh the instance to get the auto-generated id
            
            if role_name == "SUPER_ADMIN":
                super_admin_id = new_role.id        # Capture the SUPER_ADMIN id

        else:
            # If the role already exists, check if it is SUPER_ADMIN and fetch the id
            if role_name == "SUPER_ADMIN":
                super_admin_id = existing_role.id

            

    # Check if admin already exists
    super_admin = db.query(Admin).filter_by(email="superadmin@example.com").first()

    if not super_admin:
        
        super_admin = Admin(name="Super Admin", email="superadmin@example.com", password=hash_password("superadmin@123"), created_by=0, modified_by=0, role_id=super_admin_id)
        
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)