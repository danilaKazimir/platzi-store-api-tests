from http import HTTPStatus

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import CategoryResponseDto
from src.utils.assertions import assert_entity_not_found


@pytest.mark.anyio
@allure.feature("Categories")
@allure.story("Delete Category")
class TestDeleteCategories:
    NOT_FOUND_CATEGORY_ID = 0

    @allure.title("Check an existing category deletion")
    async def test_delete_user(
        self, category: CategoryResponseDto, categories_client: CategoriesClient
    ) -> None:
        with allure.step("Send DELETE /categories to delete category"):
            response = await categories_client.delete_category(category.id)
            assert response.status_code == HTTPStatus.OK
            assert response.json() is True

        with allure.step("Check that category is deleted via GET /categories"):
            get_response = await categories_client.get_category_by_id(category.id)
            assert_entity_not_found(get_response)

    @allure.title("Check a non-existing category deletion")
    async def test_delete_non_existent_user(
        self, categories_client: CategoriesClient
    ) -> None:
        with allure.step("Send DELETE /categories for non-existing user"):
            response = await categories_client.delete_category(
                self.NOT_FOUND_CATEGORY_ID
            )
            assert_entity_not_found(response)
