from sqlalchemy import Column, Integer, String
from database.db_connection import Base

class Admin(Base):

    __tablename__ = "admins"


    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, index=True)
    
    username = Column(String, unique=True, index=True, nullable=False)
    
    password = Column(String, nullable=False)