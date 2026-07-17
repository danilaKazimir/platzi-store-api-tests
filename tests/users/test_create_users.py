from http import HTTPStatus

import allure
import pytest

from src.clients.users_client import UsersClient
from src.models.users import CreateUserRequestDto, UserResponseDto


@pytest.mark.anyio
@allure.feature("Users")
@allure.story("Create User")
class TestCreateUsers:
    @allure.title("Check a new user creation")
    async def test_create_user(self, users_client: UsersClient) -> None:
        with allure.step("Send POST /users to create new user"):
            request: CreateUserRequestDto = CreateUserRequestDto()
            response = await users_client.create_user(request)
            assert response.status_code == HTTPStatus.CREATED

        with allure.step("Check that the new user exists via GET /users"):
            response_model = UserResponseDto.model_validate_json(response.content)
            assert response_model.name == request.name
            assert response_model.email == request.email
            assert response_model.password == request.password
            assert response_model.avatar == request.avatar
