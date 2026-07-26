from http import HTTPStatus

import allure
import pytest

from src.clients.products_client import ProductsClient
from src.models.products import ProductResponseDto, ProductsResponseDto
from src.utils.assertions import assert_entity_not_found


@pytest.mark.anyio
@allure.tag("api", "products")
@allure.parent_suite("API Tests")
@allure.suite("Products")
@allure.sub_suite("Get Products")
@allure.feature("Products")
@allure.story("Get Products")
class TestGetProducts:
    NOT_FOUND_PRODUCT_ID = 0
    NOT_FOUND_PRODUCT_SLUG = "___invalid___"

    @allure.title("Check get all products")
    async def test_get_all_products(
        self, product_fx: ProductResponseDto, products_client: ProductsClient
    ) -> None:
        with allure.step("Send GET /products to get all products"):
            response = await products_client.get_all_products()

        with allure.step("Check GET /products response"):
            assert response.status_code == HTTPStatus.OK
            products = ProductsResponseDto.model_validate_json(response.content)
            assert products.root
            assert product_fx in products.root

    @allure.title("Check get product by ID")
    async def test_get_product_by_id(
        self, product_fx: ProductResponseDto, products_client: ProductsClient
    ) -> None:
        with allure.step(f"Send GET /products/{product_fx.id} request"):
            response = await products_client.get_single_product_by_id(product_fx.id)

        with allure.step("Check response"):
            assert response.status_code == HTTPStatus.OK

            response_model = ProductResponseDto.model_validate_json(response.content)
            assert response_model == product_fx

    @allure.title("Check get a non-existing product by ID")
    async def test_get_non_existent_product_by_id(
        self, products_client: ProductsClient
    ) -> None:
        with allure.step(
            f"Send GET /products/{self.NOT_FOUND_PRODUCT_ID} request for "
            f"non-existent product"
        ):
            response = await products_client.get_single_product_by_id(
                self.NOT_FOUND_PRODUCT_ID
            )
            assert_entity_not_found(response)

    @allure.title("Check get product by slug")
    async def test_get_product_by_slug(
        self, product_fx: ProductResponseDto, products_client: ProductsClient
    ) -> None:
        with allure.step(f"Send GET /products/slug/{product_fx.slug} request"):
            response = await products_client.get_single_product_by_slug(product_fx.slug)

        with allure.step("Check response"):
            assert response.status_code == HTTPStatus.OK

            response_model = ProductResponseDto.model_validate_json(response.content)
            assert response_model == product_fx

    @allure.title("Check get a non-existing product by slug")
    async def test_get_non_existent_product_by_slug(
        self, products_client: ProductsClient
    ) -> None:
        with allure.step(
            f"Send GET /products/{self.NOT_FOUND_PRODUCT_SLUG} request for "
            f"non-existent product"
        ):
            response = await products_client.get_single_product_by_slug(
                self.NOT_FOUND_PRODUCT_SLUG
            )
            assert_entity_not_found(response)
