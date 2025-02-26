from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from database.db_connection import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Admin(Base):

    __tablename__ = "admins"


    id = Column(Integer, primary_key = True, index = True)
    
    name = Column(String, index = True)
    
    email = Column(String, unique = True, index = True, nullable = False)
    
    password = Column(String, nullable = False)

    created_by = Column(Integer, nullable = False)

    modified_by = Column(Integer, nullable = False)

    created_date = Column(DateTime, default = datetime.now())

    modified_date = Column(DateTime, default = datetime.now())

    is_deleted = Column(Boolean, default = False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable = False)  # Role assigned to user


    # Relationship with Role table
    role = relationship("Role", back_populates = "admin")