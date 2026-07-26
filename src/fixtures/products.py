from collections.abc import AsyncIterator
from http import HTTPStatus

import allure
import pytest

from src.clients.products_client import ProductsClient
from src.models.categories import CategoryResponseDto
from src.models.products import CreateProductRequestDto, ProductResponseDto


@pytest.fixture
@allure.title("Create a new product for tests")
async def product_fx(
    category_fx: CategoryResponseDto,
    products_client: ProductsClient,
) -> AsyncIterator[ProductResponseDto]:
    request = CreateProductRequestDto(category_id=category_fx.id)
    response = await products_client.create_product(request)

    assert response.status_code == HTTPStatus.CREATED

    product = ProductResponseDto.model_validate_json(response.content)

    yield product

    checked_product = await products_client.get_single_product_by_id(product.id)
    if checked_product.status_code == HTTPStatus.OK:
        await products_client.delete_product(product.id)
