from http import HTTPStatus

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.fixtures.products import ProductFactory
from src.models.categories import CategoriesResponseDto, CategoryResponseDto
from src.models.products import CreateProductRequestDto, ProductsResponseDto
from src.utils.assertions import assert_entity_not_found
from tests.test_data.common import LOOKUP_FIELD_PARAMS, LookupField


@allure.tag("api", "categories")
@allure.parent_suite("API Tests")
@allure.suite("Categories")
@allure.sub_suite("Get Categories")
@allure.feature("Categories")
@allure.story("Get Categories")
class TestGetCategories:
    NOT_FOUND_CATEGORY_ID = 0
    NOT_FOUND_CATEGORY_SLUG = "___invalid___"

    @allure.title("Check get list of all categories")
    async def test_get_all_categories(
        self, category_fx: CategoryResponseDto, categories_client: CategoriesClient
    ) -> None:
        with allure.step("Send GET /categories to get all categories"):
            response = await categories_client.get_all_categories()

        with allure.step("Check GET /categories response"):
            assert response.status_code == HTTPStatus.OK
            categories = CategoriesResponseDto.model_validate_json(response.content)
            assert category_fx in categories.root

    @allure.title("Check get single category by {param_id}")
    @pytest.mark.parametrize("get_by", LOOKUP_FIELD_PARAMS)
    async def test_get_single_category(
        self,
        categories_client: CategoriesClient,
        get_by: LookupField,
        category_fx: CategoryResponseDto,
    ) -> None:
        if get_by == "id":
            with allure.step(f"Send GET /category{category_fx.id} to get category "):
                response = await categories_client.get_category_by_id(category_fx.id)
        else:
            with allure.step(f"Send GET /category{category_fx.slug} to get category "):
                response = await categories_client.get_category_by_slug(
                    category_fx.slug
                )

        with allure.step("Check GET /categories response"):
            assert response.status_code == HTTPStatus.OK
            received_category = CategoryResponseDto.model_validate_json(
                response.content
            )
            assert received_category == category_fx

    @allure.title("Check get all products by category")
    async def test_get_all_products_by_category(
        self,
        category_fx: CategoryResponseDto,
        product_factory: ProductFactory,
        categories_client: CategoriesClient,
    ) -> None:
        expected_products_count = 4
        with allure.step("Create four product with same category"):
            same_category_products = [
                await product_factory(
                    CreateProductRequestDto(category_id=category_fx.id)
                )
                for _ in range(expected_products_count)
            ]

        with allure.step(
            f"Send GET /categories/{category_fx.id}/products to get all products"
        ):
            response = await categories_client.get_all_products_by_category(
                category_fx.id
            )

        with allure.step(f"Check GET /categories/{category_fx.id}/products response"):
            assert response.status_code == HTTPStatus.OK
            assert len(response.json()) == expected_products_count
            response_model = ProductsResponseDto.model_validate_json(response.content)
            assert same_category_products == response_model.root

    @allure.title("Check get all products by category when category have 0 products")
    async def test_get_zero_products_by_category(
        self, category_fx: CategoryResponseDto, categories_client: CategoriesClient
    ) -> None:
        expected_products_count = 0
        with allure.step(
            f"Send GET /categories/{category_fx.id}/products to get all products"
        ):
            response = await categories_client.get_all_products_by_category(
                category_fx.id
            )

        with allure.step(f"Check GET /categories/{category_fx.id}/products response"):
            assert response.status_code == HTTPStatus.OK
            assert len(response.json()) == expected_products_count

    @allure.title("Check get a non-existing category by {param_id}")
    @pytest.mark.parametrize("get_by", LOOKUP_FIELD_PARAMS)
    async def test_get_non_existent_category(
        self, categories_client: CategoriesClient, get_by: LookupField
    ) -> None:
        if get_by == "id":
            with allure.step(
                f"Send GET /categories/{self.NOT_FOUND_CATEGORY_ID} for "
                f"a non-existing category"
            ):
                response = await categories_client.get_category_by_id(
                    self.NOT_FOUND_CATEGORY_ID
                )
        else:
            with allure.step(
                f"Send GET /categories/slug/{self.NOT_FOUND_CATEGORY_SLUG} for "
                f"a non-existing category"
            ):
                response = await categories_client.get_category_by_slug(
                    self.NOT_FOUND_CATEGORY_SLUG
                )
        assert_entity_not_found(response)
