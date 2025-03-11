import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Enum, func
from sqlalchemy.orm import relationship

from database.db_connection import Base
from model.user_status import UserStatus


class User(Base):

    __tablename__ = "users"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = Column(Integer, unique = True, index = True, nullable = True, default=None)

    firstname = Column(String, nullable = True)

    lastname = Column(String, nullable = True)

    email = Column(String, unique = True, index = True, nullable = False)

    password = Column(String, nullable = False)

    created_date = Column(DateTime, server_default=func.now())
    
    modified_date = Column(DateTime, server_default=func.now(), onupdate=func.now())

    verified_by = Column(UUID(as_uuid=True), nullable=True)

    status = Column(Enum(UserStatus, native_enum=False), default=UserStatus.PENDING.value)

    is_deleted = Column(Boolean, default = False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable = False)


    # Relationship with Role table
    role = relationship("Role", back_populates = "user")