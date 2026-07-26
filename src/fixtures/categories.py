from collections.abc import AsyncIterator
from http import HTTPStatus

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import CategoryResponseDto, CreateCategoryRequestDto


@pytest.fixture
@allure.title("Create a new category for tests")
async def category_fx(
    categories_client: CategoriesClient,
) -> AsyncIterator[CategoryResponseDto]:
    request = CreateCategoryRequestDto()
    response = await categories_client.create_category(request)

    assert response.status_code == HTTPStatus.CREATED

    category = CategoryResponseDto.model_validate_json(response.content)

    yield category

    checked_category = await categories_client.get_category_by_id(category.id)
    if checked_category.status_code == HTTPStatus.OK:
        await categories_client.delete_category(category.id)
