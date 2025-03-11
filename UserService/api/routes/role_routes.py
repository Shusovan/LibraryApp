from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db_connection import get_db
from model.role import Role
from schema.role_schema import RoleCreate, RoleNameResponse, RoleResponse
from service.role_service import get_role_by_id


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

    # return roles
    
    return [RoleResponse(id=role.id, name=role.name) for role in roles]


# get role by id
@router.get("/get-role/{id}", response_model=RoleNameResponse)
def get_role(id: int, db: Session = Depends(get_db)):

    role_name = get_role_by_id(db, id)

    if not role_name:
        raise HTTPException(status_code=404, detail="Admin not found")

    return role_name