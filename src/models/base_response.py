from pydantic import BaseModel, Field


class BaseResponseDto(BaseModel):
    creation_at: str = Field(alias="creationAt")
    updated_at: str = Field(alias="updatedAt")
