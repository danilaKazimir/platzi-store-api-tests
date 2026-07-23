from http import HTTPStatus

import allure
import pytest

from src.clients.products_client import ProductsClient
from src.models.categories import CategoryResponseDto
from src.models.products import CreateProductRequestDto, ProductResponseDto


@pytest.mark.anyio
@allure.tag("api", "products")
@allure.parent_suite("API Tests")
@allure.suite("Products")
@allure.sub_suite("Create Products")
@allure.feature("Products")
@allure.story("Create Products")
class TestCreateProduct:
    @allure.title("Create a new product creation")
    async def test_create_product(
        self, category_fx: CategoryResponseDto, products_client: ProductsClient
    ) -> None:
        with allure.step("Send POST /products request"):
            request: CreateProductRequestDto = CreateProductRequestDto(
                category_id=category_fx.id
            )
            response = await products_client.create_product(request)

        with allure.step("Check response"):
            assert response.status_code == HTTPStatus.CREATED

            response_model = ProductResponseDto.model_validate_json(response.content)
            assert response_model.title == request.title
            assert response_model.slug == "-".join(request.title.split(" ")).lower()
            assert response_model.price == request.price
            assert response_model.description == request.description
            assert response_model.images == request.images
            assert response_model.category == category_fx
