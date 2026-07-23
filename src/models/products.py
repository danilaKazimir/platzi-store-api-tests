from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from src.models.base_response import BaseResponseDto
from src.models.categories import CategoryResponseDto
from src.utils.fake_data import fake


class CreateProductRequestDto(BaseModel):
    model_config = ConfigDict(serialize_by_alias=True)

    title: str = Field(default_factory=fake.generate_product_title)
    price: int = Field(default_factory=fake.generate_product_price)
    description: str = Field(default_factory=fake.generate_product_description)
    category_id: int = Field(serialization_alias="categoryId")
    images: list[str] = Field(default_factory=fake.generate_product_images)


class ProductResponseDto(BaseResponseDto):
    title: str
    slug: str
    price: int
    description: str
    images: list[str | HttpUrl]
    category: CategoryResponseDto
    id: int
