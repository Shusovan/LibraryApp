from sqlalchemy import Column, ForeignKey, Integer, String
from database.db_connection import Base
from sqlalchemy.orm import relationship


class Admin(Base):

    __tablename__ = "admins"


    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, index=True)
    
    email = Column(String, unique=True, index=True, nullable=False)
    
    password = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # Role assigned to user


    # Relationship with Role table
    role = relationship("Role", back_populates="admin")