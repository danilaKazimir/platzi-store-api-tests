from http import HTTPStatus
from uuid import uuid4

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import CategoryResponseDto, CreateCategoryRequestDto


@pytest.mark.anyio
@allure.tag("api", "categories")
@allure.parent_suite("API Tests")
@allure.suite("Categories")
@allure.sub_suite("Create Categories")
@allure.feature("Categories")
@allure.story("Create Categories")
class TestCreateCategories:
    @allure.title("Check a new category creation {param_id}")
    @pytest.mark.parametrize(
        ("name", "expected_slug"),
        [
            pytest.param(
                "testCategory",
                "testcategory",
                id="category without whitespaces",
            ),
            pytest.param(
                "test Category",
                "test-category",
                id="category with whitespaces",
            ),
        ],
    )
    async def test_create_categories(
        self, categories_client: CategoriesClient, name: str, expected_slug: str
    ) -> None:
        with allure.step("Send POST /categories to create new user"):
            unique_suffix = uuid4().hex
            request = CreateCategoryRequestDto(name=f"{name}{unique_suffix}")
            response = await categories_client.create_category(request)
            assert response.status_code == HTTPStatus.CREATED

        with allure.step("Check that the new categories exists via GET /categories"):
            response_model = CategoryResponseDto.model_validate_json(response.content)
            assert response_model.name == request.name
            assert response_model.image == request.image
            assert response_model.slug == f"{expected_slug}{unique_suffix}"
