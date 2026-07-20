from http import HTTPStatus

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import CategoryResponseDto, CreateCategoryRequestDto


@pytest.fixture
@allure.title("Create a new category for tests")
async def category(
    categories_client: CategoriesClient,
) -> CategoryResponseDto:
    request = CreateCategoryRequestDto()
    response = await categories_client.create_category(request)

    assert response.status_code == HTTPStatus.CREATED

    return CategoryResponseDto.model_validate_json(response.content)
