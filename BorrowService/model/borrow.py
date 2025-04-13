import datetime
import uuid
from sqlalchemy import UUID, Column, Date, Enum, Integer, String
from core.db_connection import Base
from model.borrow_status import BorrowStatus


class BorrowRecords(Base):

    __tablename__ = "borrow"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = Column(Integer, unique = True, index = True, nullable = False)

    book_id = Column(String, unique=True, index=True, nullable=False)

    request_id = Column(UUID(as_uuid=True), index=True, unique=True, nullable=False)

    borrow_date = Column(Date)

    # mark this as due_date
    return_date = Column(Date)

    # return_date = Column(DateTime)

    status = Column(Enum(BorrowStatus, native_enum=False), default=BorrowStatus.PENDING.value)

    # approval_required = Column(String, nullable=True)      # approval for EXCLUSIVE books only

    # update after due_date is crossed
    # compare return_date and due_date, get the fine value ($5/day)
    # fine = Column(Integer, nullable = True, default = None)

