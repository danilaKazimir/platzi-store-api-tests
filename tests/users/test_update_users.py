from http import HTTPStatus

import allure
import pytest

from src.clients.users_client import UsersClient
from src.models.users import UpdateUserRequestDto, UserResponseDto
from src.utils.assertions import assert_entity_not_found


@pytest.mark.anyio
@allure.feature("Users")
@allure.story("Update User")
class TestUpdateUsers:
    NOT_FOUND_USER_ID = 0

    @allure.title("Check an existing user update, {param_id}")
    @pytest.mark.parametrize(
        "request_dto",
        [
            pytest.param(UpdateUserRequestDto(), id="with all body fields"),
            pytest.param(UpdateUserRequestDto(email=None), id="without email field"),
            pytest.param(UpdateUserRequestDto(name=None), id="without name"),
        ],
    )
    async def test_update_user(
        self,
        user: UserResponseDto,
        users_client: UsersClient,
        request_dto: UpdateUserRequestDto,
    ) -> None:
        with allure.step(
            f"Send PUT /users/{user.id} with {request_dto.name}, {request_dto.email}"
        ):
            response = await users_client.update_user(user.id, request_dto)
            assert response.status_code == HTTPStatus.OK

        with allure.step("Check response"):
            response_model = UserResponseDto.model_validate_json(response.content)
            if request_dto.name:
                assert response_model.name == request_dto.name
            else:
                assert response_model.name == user.name
            if request_dto.email:
                assert response_model.email == request_dto.email
            else:
                assert response_model.email == user.email
            assert response_model.model_dump(
                exclude={"name", "email", "updated_at"}
            ) == user.model_dump(exclude={"name", "email", "updated_at"})

        with allure.step("Check user was updated successfully"):
            get_response = await users_client.get_single_user(user.id)
            assert get_response.status_code == HTTPStatus.OK
            get_response_model = UserResponseDto.model_validate_json(
                get_response.content
            )
            if request_dto.name:
                assert get_response_model.name == request_dto.name
            else:
                assert get_response_model.name == user.name
            if request_dto.email:
                assert get_response_model.email == request_dto.email
            else:
                assert get_response_model.email == user.email
            assert response_model.model_dump(
                exclude={"name", "email", "updated_at"}
            ) == user.model_dump(exclude={"name", "email", "updated_at"})

    @allure.title("Check a non-existing user update")
    async def test_update_non_existent_user(self, users_client: UsersClient) -> None:
        with allure.step("Send PUT /users request for a non-existing user"):
            response = await users_client.update_user(
                self.NOT_FOUND_USER_ID, UpdateUserRequestDto()
            )
            assert_entity_not_found(response)
