from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db_connection import Base


class Role(Base):
    
    __tablename__ = "roles"


    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, unique=True, index=True, nullable=False)  # Example: "TEACHER", "USER", "RESEARCHER", "GUEST"


    # Explicitly define the back_populates relationship
    user = relationship("User", back_populates="role", cascade="all, delete")