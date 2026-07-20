from pydantic import BaseModel, ConfigDict, Field, HttpUrl, RootModel

from src.models.base_response import BaseResponseDto
from src.utils.fake_data import fake


class BaseCategoryRequestDto(BaseModel):
    name: str | None = Field(default_factory=fake.generate_unique_category)
    image: str | HttpUrl | None = Field(default_factory=fake.generate_url)


class CreateCategoryDto(BaseCategoryRequestDto):
    pass


class UpdateCategoryDto(BaseCategoryRequestDto):
    pass


class CategoryResponseDto(BaseResponseDto):
    id: int
    name: str
    slug: str
    image: str | HttpUrl


class CategoriesResponseDto(RootModel[list[CategoryResponseDto]]):
    model_config = ConfigDict(strict=True)

    pass
