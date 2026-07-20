from pydantic import BaseModel, Field, EmailStr


class LoginRequestDto(BaseModel):
    email: str | EmailStr | None
    password: str | None


class LoginResponseDto(BaseModel):
    access_token: str
    refresh_token: str


class UnauthorizedError(BaseModel):
    message: str
    status_code: int = Field(alias="statusCode")
