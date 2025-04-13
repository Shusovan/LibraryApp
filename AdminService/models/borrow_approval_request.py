from datetime import datetime
from sqlalchemy import UUID, Column, DateTime, Integer, String
from database.db_connection import Base


class BorrowApprovalRequest(Base):

    __tablename__ = "borrowrecords"


    request_id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)

    user_id = Column(Integer, unique = False, index = True, nullable = False)

    book_id = Column(String, unique=False, index=True, nullable=False)

    approved_by = Column(UUID(as_uuid=True), nullable=True)

    received_date = Column(DateTime, default = datetime.now())

    approved_date = Column(DateTime, nullable=True)

    approval_status = Column(String, nullable=False)