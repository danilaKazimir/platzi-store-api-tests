from http import HTTPStatus

import allure
import pytest

from src.clients.categories_client import CategoriesClient
from src.models.categories import (
    CategoryResponseDto,
    UpdateCategoryRequestDto,
)
from src.utils.assertions import assert_entity_not_found, assert_not_null_constraint


@pytest.mark.anyio
@allure.tag("api", "categories")
@allure.parent_suite("API Tests")
@allure.suite("Categories")
@allure.sub_suite("Update Categories")
@allure.feature("Categories")
@allure.story("Update Categories")
class TestUpdateCategories:
    NOT_FOUND_CATEGORY_ID = 0

    @allure.title("Check an existing category update, {param_id}")
    @pytest.mark.parametrize(
        "request_dto",
        [
            pytest.param(UpdateCategoryRequestDto(), id="with all body fields"),
            pytest.param(UpdateCategoryRequestDto(name=None), id="without name field"),
            pytest.param(
                UpdateCategoryRequestDto(image=None), id="without image field"
            ),
        ],
    )
    async def test_categories_update(
        self,
        category_fx: CategoryResponseDto,
        categories_client: CategoriesClient,
        request_dto: UpdateCategoryRequestDto,
    ) -> None:
        if request_dto.name and request_dto.image:
            with allure.step(
                f"Send PUT /categories/{category_fx.id} "
                f"with category {request_dto.name}, {request_dto.image}"
            ):
                response = await categories_client.update_category(
                    category_fx.id, request_dto
                )
                assert response.status_code == HTTPStatus.OK

            with allure.step("Check response"):
                response_model = CategoryResponseDto.model_validate_json(
                    response.content
                )
                if request_dto.name:
                    assert response_model.name == request_dto.name
                else:
                    assert response_model.name == category_fx.name
                if request_dto.image:
                    assert response_model.image == request_dto.image
                else:
                    assert response_model.image == category_fx.image

            with allure.step("Check category was updated successfully"):
                get_response = await categories_client.get_category_by_id(
                    category_fx.id
                )
                assert get_response.status_code == HTTPStatus.OK
                get_response_model = CategoryResponseDto.model_validate_json(
                    get_response.content
                )
                if request_dto.name:
                    assert get_response_model.name == request_dto.name
                else:
                    assert get_response_model.name == category_fx.name
                if request_dto.image:
                    assert get_response_model.image == request_dto.image
                else:
                    assert get_response_model.image == category_fx.image
        else:
            with allure.step(
                f"Send PUT /categories/{category_fx.id} "
                f"with category {request_dto.name}, {request_dto.image}"
            ):
                response = await categories_client.update_category(
                    category_fx.id, request_dto
                )
                assert_not_null_constraint(response)

    @allure.title("Check a non-existing user update")
    async def test_update_non_existent_user(
        self, categories_client: CategoriesClient
    ) -> None:
        with allure.step("Send PUT /categories request for a non-existing category"):
            response = await categories_client.update_category(
                self.NOT_FOUND_CATEGORY_ID, UpdateCategoryRequestDto()
            )
            assert_entity_not_found(response)
