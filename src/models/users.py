from pydantic import BaseModel, EmailStr, Field, HttpUrl, RootModel


class BaseUserDate(BaseModel):
    email: EmailStr
    name: str


class CreateUser(BaseUserDate):
    password: str
    avatar: HttpUrl


class UserResponse(CreateUser):
    id: int
    role: str
    creation_at: str = Field(alias="creationAt")
    updated_at: str = Field(alias="updatedAt")


class UsersResponse(RootModel[list[UserResponse]]):
    pass
