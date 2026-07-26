from http import HTTPStatus

import allure
import pytest

from src.clients.products_client import ProductsClient
from src.models.products import ProductResponseDto, UpdateProductRequestDto
from src.utils.fake_data import fake


@pytest.mark.anyio
@allure.tag("api", "products")
@allure.parent_suite("API Tests")
@allure.suite("Products")
@allure.sub_suite("Update Products")
@allure.feature("Products")
@allure.story("Update Products")
class TestUpdateProducts:
    @allure.title("Check an existing product update")
    @pytest.mark.xfail(reason="UPDATE /products return 500 Internal Server Error")
    async def test_update_product(
        self, product_fx: ProductResponseDto, products_client: ProductsClient
    ) -> None:
        with allure.step(f"Send UPDATE /products/{product_fx.id} to update category"):
            request = UpdateProductRequestDto(
                title=fake.generate_product_title(), price=fake.generate_product_price()
            )
            response = await products_client.update_product(product_fx.id, request)

        with allure.step(f"Check UPDATE /products/{product_fx.id} response"):
            assert response.status_code == HTTPStatus.OK

            response_model = ProductResponseDto.model_validate_json(response.content)
            assert request.title == response_model.title
            assert request.price == response_model.price
