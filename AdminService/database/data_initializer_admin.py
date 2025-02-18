from sqlalchemy.orm import session

from models.admin import Admin
from security.encrypt import hash_password
from config.notify_role_creation import request_role_creation


# pre-populate SUPER_ADMIN to database
def initialize_admin(db : session):

    # Check if admin already exists
    superadmin = db.query(Admin).filter_by(username="superadmin").first()

    if not superadmin:
        superadmin = Admin(name="Super Admin", username="superadmin", password=hash_password("superadmin123"))
        db.add(superadmin)
        db.commit()
        db.refresh(superadmin)


    # request SecurityService for role creation
    request_role_creation(superadmin.username, "SUPER_ADMIN")