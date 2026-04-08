from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: str


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

# Setting up Pydantic models for response


class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    role: str

    # True when db data directly returns for Dict False or can this removed or True also will work
    model_config = ConfigDict(from_attributes=True)  # Check the usage of this?


class EmployeesResponse(BaseModel):
    message: str
    payload: List[UserResponse]
