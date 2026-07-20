from http import HTTPStatus
from uuid import uuid4

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import CategoryResponseDto, CreateCategoryDto


@pytest.mark.anyio
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
        unique_suffix = uuid4().hex
        request = CreateCategoryDto(name=f"{name}{unique_suffix}")
        response = await categories_client.create_category(request)
        assert response.status_code == HTTPStatus.CREATED

        response_model = CategoryResponseDto.model_validate_json(response.content)
        assert response_model.name == request.name
        assert response_model.image == request.image
        assert response_model.slug == f"{expected_slug}{unique_suffix}"
