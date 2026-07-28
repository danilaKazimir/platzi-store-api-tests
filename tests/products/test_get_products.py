from http import HTTPStatus
from typing import Literal

import allure
import pytest

from src.clients.products_client import ProductsClient
from src.fixtures.categories import CategoryFactory
from src.fixtures.products import ProductFactory
from src.models.categories import CategoryResponseDto
from src.models.products import (
    CreateProductRequestDto,
    ProductResponseDto,
    ProductsResponseDto,
)
from src.utils.assertions import assert_entity_not_found


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

    @allure.title("Check get products {param_id}")
    @pytest.mark.parametrize(
        ("offset", "limit"),
        [
            pytest.param(0, None, id="with offset query param"),
            pytest.param(None, 3, id="with limit query param"),
            pytest.param(1, 3, id="with limit and offset query param"),
        ],
    )
    async def test_get_products_with_filters(
        self, products_client: ProductsClient, offset: int, limit: int
    ) -> None:
        with allure.step(
            f"Send GET /products request with offset:{offset}, limit:{limit}"
        ):
            response = await products_client.get_all_products(
                offset=offset, limit=limit
            )

        with allure.step("Check response"):
            assert response.status_code == HTTPStatus.OK
            products = ProductsResponseDto.model_validate_json(response.content)
            assert products.root

    @allure.title("Check get products related by: {param_id}")
    @pytest.mark.parametrize(
        "related_by",
        [
            pytest.param("id", id="id"),
            pytest.param("slug", id="slug"),
        ],
    )
    async def test_get_related_products(
        self,
        products_client: ProductsClient,
        category_fx: CategoryResponseDto,
        product_factory: ProductFactory,
        category_factory: CategoryFactory,
        related_by: Literal["id", "slug"],
    ) -> None:
        same_category_products = [
            await product_factory(CreateProductRequestDto(category_id=category_fx.id))
            for _ in range(3)
        ]
        source_product, *expected_related_products = same_category_products

        unrelated_category = await category_factory()
        await product_factory(
            CreateProductRequestDto(category_id=unrelated_category.id)
        )

        if related_by == "id":
            endpoint = f"/products/{source_product.id}/related"

            with allure.step(f"Send GET {endpoint} request"):
                response = await products_client.get_products_related_by_id(
                    source_product.id
                )
        else:
            endpoint = f"/products/slug/{source_product.slug}/related"

            with allure.step(f"Send GET {endpoint} request"):
                response = await products_client.get_products_related_by_slug(
                    source_product.slug
                )

        with allure.step("Check response"):
            assert response.status_code == HTTPStatus.OK
            response_model = ProductsResponseDto.model_validate_json(response.content)

        with allure.step("Check related products"):
            actual_products = {
                product.id: product.model_dump(mode="json")
                for product in response_model.root
            }
            expected_products = {
                product.id: product.model_dump(mode="json")
                for product in expected_related_products
            }

            assert actual_products == expected_products, (
                "Related products response does not match expected products"
            )
