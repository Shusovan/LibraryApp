from enum import Enum as PyEnum


class BorrowStatus(PyEnum):
    
    PENDING = "PENDING"
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"