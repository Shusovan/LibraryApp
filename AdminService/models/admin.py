import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from database.db_connection import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Admin(Base):

    __tablename__ = "admins"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    
    name = Column(String, index = True)
    
    email = Column(String, unique = True, index = True, nullable = False)
    
    password = Column(String, nullable = False)

    created_by = Column(UUID(as_uuid=True), nullable = True)

    modified_by = Column(UUID(as_uuid=True), nullable = True)

    created_date = Column(DateTime, default = datetime.now())

    modified_date = Column(DateTime, default = datetime.now())

    is_deleted = Column(Boolean, default = False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable = False)  # Role assigned to user


    # Relationship with Role table
    role = relationship("Role", back_populates = "admin")