from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, RootModel

from src.utils.fake_data import fake


class BaseUserRequestDto(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str | None = Field(default_factory=fake.generate_name)
    email: EmailStr | None = Field(default_factory=fake.generate_email)


class CreateUserRequestDto(BaseUserRequestDto):
    password: str | None = Field(default_factory=fake.generate_password)
    avatar: str | None = Field(default_factory=fake.generate_avatar_url)


class UpdateUserRequestDto(BaseUserRequestDto):
    pass


class UserResponseDto(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    email: EmailStr | str
    password: str
    name: str
    role: str
    avatar: HttpUrl | str
    creation_at: str = Field(alias="creationAt")
    updated_at: str = Field(alias="updatedAt")


class UsersResponseDto(RootModel[list[UserResponseDto]]):
    model_config = ConfigDict(strict=True)

    pass
