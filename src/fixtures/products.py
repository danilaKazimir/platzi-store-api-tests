from collections.abc import AsyncIterator, Awaitable
from http import HTTPStatus
from typing import Protocol

import allure
import pytest

from src.clients.products_client import ProductsClient
from src.models.categories import CategoryResponseDto
from src.models.products import CreateProductRequestDto, ProductResponseDto


class ProductFactory(Protocol):
    def __call__(
        self, product_dto: CreateProductRequestDto | None = None
    ) -> Awaitable[ProductResponseDto]: ...


@pytest.fixture
@allure.title("Create products for tests")
async def product_factory(
    category_fx: CategoryResponseDto,
    products_client: ProductsClient,
) -> AsyncIterator[ProductFactory]:
    created_product_ids: list[int] = []

    async def create_product(
        product_dto: CreateProductRequestDto | None = None,
    ) -> ProductResponseDto:
        request = (
            product_dto
            if product_dto is not None
            else CreateProductRequestDto(category_id=category_fx.id)
        )
        response = await products_client.create_product(request)

        assert response.status_code == HTTPStatus.CREATED

        product = ProductResponseDto.model_validate_json(response.content)
        created_product_ids.append(product.id)

        return product

    yield create_product

    for product_id in reversed(created_product_ids):
        checked_product = await products_client.get_single_product_by_id(product_id)
        if checked_product.status_code == HTTPStatus.OK:
            await products_client.delete_product(product_id)


@pytest.fixture
@allure.title("Create a new product for tests")
async def product_fx(product_factory: ProductFactory) -> ProductResponseDto:
    return await product_factory()
