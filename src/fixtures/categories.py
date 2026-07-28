from collections.abc import AsyncIterator, Awaitable
from http import HTTPStatus
from typing import Protocol

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import CategoryResponseDto, CreateCategoryRequestDto


class CategoryFactory(Protocol):
    def __call__(
        self, category_dto: CreateCategoryRequestDto | None = None
    ) -> Awaitable[CategoryResponseDto]: ...


@pytest.fixture
@allure.title("Create categories for tests")
async def category_factory(
    categories_client: CategoriesClient,
) -> AsyncIterator[CategoryFactory]:
    created_category_ids: list[int] = []

    async def create_category(
        category_dto: CreateCategoryRequestDto | None = None,
    ) -> CategoryResponseDto:
        request = (
            category_dto if category_dto is not None else CreateCategoryRequestDto()
        )
        response = await categories_client.create_category(request)

        assert response.status_code == HTTPStatus.CREATED

        category = CategoryResponseDto.model_validate_json(response.content)
        created_category_ids.append(category.id)

        return category

    yield create_category

    for category_id in reversed(created_category_ids):
        checked_category = await categories_client.get_category_by_id(category_id)
        if checked_category.status_code == HTTPStatus.OK:
            await categories_client.delete_category(category_id)


@pytest.fixture
@allure.title("Create a new category for tests")
async def category_fx(category_factory: CategoryFactory) -> CategoryResponseDto:
    return await category_factory()
