from sqlalchemy.orm import Session

from model.role import Role


def get_role_by_id(db: Session, id: int):

    return db.query(Role).filter(Role.id == id).first()