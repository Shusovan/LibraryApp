from enum import Enum as PyEnum


class BookStatus(PyEnum):
    
    PENDING = "PENDING"
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"