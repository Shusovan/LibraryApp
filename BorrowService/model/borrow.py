from datetime import date, timedelta
import uuid
from sqlalchemy import UUID, Column, DateTime, Enum, Integer, String
from core.db_connection import Base
from model import borrow_status
from model.borrow_status import BookStatus


class BorrowRecords(Base):

    __tablename__ = "borrow"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = Column(Integer, unique = True, index = True, nullable = False)

    book_id = Column(String, unique=True, index=True, nullable=False)

    request_id = Column(UUID(as_uuid=True), index=True, unique=True, nullable=False)

    borrow_date = Column(DateTime)

    return_date = Column(DateTime)

    status = Column(Enum(BookStatus, native_enum=False), default=BookStatus.PENDING.value)

    # approval_required = Column(String, nullable=True)      # approval for EXCLUSIVE books only

    # fine = Column(Integer, nullable = True, default = None)

