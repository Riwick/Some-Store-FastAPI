from fastapi_users import schemas
from pydantic import Field, EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(max_length=30)
    email: EmailStr
    password: str = Field(max_length=100)
