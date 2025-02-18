from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connection import Base

class User(Base):
    
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, unique=True, index=True, nullable=False)
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # Role assigned to user

    # Relationship with Role table
    role = relationship("Role", back_populates="users")