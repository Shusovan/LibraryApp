from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    name: str

    class Config:
        from_attributes = True

class RoleNameResponse(RoleBase):
    name: str

    class Config:
        from_attributes = True