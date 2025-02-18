from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db_connection import get_db
from models.role import Role
from schemas.role_schema import RoleCreate, RoleResponse
from models.user import User
from schemas.user_schema import AssignRoleRequest


router = APIRouter()


@router.post("/create-role", response_model=dict)
def add_role(role: RoleCreate, db: Session = Depends(get_db)):
    
    existing_role = db.query(Role).filter_by(name = role.name).first()

    if existing_role:
        return {"message" : "role already exists"}
    
    new_role = Role(name = role.name)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return {"message" : "new role addedd successfully"}


@router.get("/get-roles", response_model=list[RoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    
    roles = db.query(Role).all()     # find all roles from database
    
    return [RoleResponse(id=role.id, name=role.name) for role in roles]


# Assign a pre-defined role to a user when requested by AdminService
@router.post("/assign-role", response_model=dict)
def assign_role(request: AssignRoleRequest, db: Session = Depends(get_db)):

    # Fetch predefined role from the database
    role = db.query(Role).filter_by(name=request.role_name).first()
    
    if not role:
        raise HTTPException(status_code=400, detail=f"Role '{request.role_name}' not found")

    # Fetch the user from the database
    user = db.query(User).filter_by(username=request.username).first()

    if not user:
        # Create a new user and assign the role if user does not exist
        user = User(username=request.username, role_id=role.id)
        db.add(user)
    
    else:
        # Update existing user role
        user.role_id = role.id

    db.commit()
    db.refresh(user)

    return {"message": f"Assigned predefined role '{role.name}' to {user.username}"}