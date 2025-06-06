from sqlalchemy import Column, Integer, String
from database.db_connection import Base
from sqlalchemy.orm import relationship


class Role(Base):
    
    __tablename__ = "roles"


    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, unique=True, index=True, nullable=False)  # Example: "superadmin", "admin"


    # Explicitly define the back_populates relationship
    admin = relationship("Admin", back_populates="role", cascade="all, delete")