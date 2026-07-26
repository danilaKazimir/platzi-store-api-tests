from http import HTTPStatus

import allure
import pytest

from src.clients.products_client import ProductsClient
from src.models.products import ProductResponseDto
from src.utils.assertions import assert_entity_not_found


@pytest.mark.anyio
@allure.tag("api", "products")
@allure.parent_suite("API Tests")
@allure.suite("Products")
@allure.sub_suite("Delete Products")
@allure.feature("Products")
@allure.story("Delete Products")
class TestDeleteProduct:
    NOT_FOUND_PRODUCT_ID = 0

    @allure.title("Check an existing product deletion")
    async def test_delete_product(
        self, product_fx: ProductResponseDto, products_client: ProductsClient
    ) -> None:
        with allure.step("Send DELETE /products to delete category"):
            response = await products_client.delete_product(product_fx.id)

        with allure.step("Check DELETE /products response"):
            assert response.status_code == HTTPStatus.OK
            assert response.json() is True

        with allure.step("Check that product is deleted via GET /products"):
            get_response = await products_client.get_single_product_by_id(product_fx.id)
            assert_entity_not_found(get_response)

    @allure.title("Check a non-existing product deletion")
    async def test_delete_product_with_product_id(
        self, products_client: ProductsClient
    ) -> None:
        with allure.step("Send DELETE /products to delete non-existent category"):
            response = await products_client.delete_product(self.NOT_FOUND_PRODUCT_ID)

        with allure.step("Check DELETE /products response"):
            assert_entity_not_found(response)
