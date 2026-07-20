from http import HTTPStatus

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import CategoriesResponseDto, CategoryResponseDto
from src.utils.assertions import assert_entity_not_found


@pytest.mark.anyio
@allure.parent_suite("API Tests")
@allure.suite("Categories")
@allure.sub_suite("Get Categories")
@allure.feature("Categories")
@allure.story("Get Categories")
class TestGetCategories:
    NOT_FOUND_CATEGORY_ID = 0

    @allure.title("Check get list of all categories")
    async def test_get_all_categories(
        self, categories_client: CategoriesClient
    ) -> None:
        with allure.step("Send GET /categories to get all categories"):
            response = await categories_client.get_all_categories()
            assert response.status_code == HTTPStatus.OK

        with allure.step("Check GET /categories response"):
            categories = CategoriesResponseDto.model_validate_json(response.content)
            assert categories.root

    @allure.title("Check get category by ID")
    async def test_get_single_category(
        self, category: CategoryResponseDto, categories_client: CategoriesClient
    ) -> None:
        with allure.step(f"Send GET /category{category.id} to get category "):
            response = await categories_client.get_category_by_id(category.id)
            assert response.status_code == HTTPStatus.OK

        with allure.step("Check GET /categories response"):
            received_category = CategoryResponseDto.model_validate_json(
                response.content
            )
            assert received_category == category

    @allure.title("Check get a non-existing category")
    async def test_get_non_existent_user(
        self, categories_client: CategoriesClient
    ) -> None:
        with allure.step(
            f"Send GET /users/{self.NOT_FOUND_CATEGORY_ID} for a non-existing category"
        ):
            response = await categories_client.get_category_by_id(
                self.NOT_FOUND_CATEGORY_ID
            )
            assert_entity_not_found(response)
