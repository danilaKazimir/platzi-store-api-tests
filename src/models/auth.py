from pydantic import BaseModel, EmailStr, Field


class LoginRequestDto(BaseModel):
    email: str | EmailStr | None
    password: str | None


class TokensResponseDto(BaseModel):
    access_token: str
    refresh_token: str


class UnauthorizedError(BaseModel):
    message: str
    status_code: int = Field(alias="statusCode")
