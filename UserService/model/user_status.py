from enum import Enum as PyEnum


class UserStatus(PyEnum):
    
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"