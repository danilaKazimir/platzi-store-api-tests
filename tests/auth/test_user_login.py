from http import HTTPStatus
from uuid import uuid4

import allure
import pytest

from src.clients.auth_client import AuthClient
from src.models.auth import LoginRequestDto, TokensResponseDto
from src.models.users import UserResponseDto
from src.utils.assertions import assert_unauthorized_error


@pytest.mark.anyio
@allure.tag("api", "auth")
@allure.parent_suite("API Tests")
@allure.suite("Auth")
@allure.sub_suite("User Login")
@allure.feature("Auth")
@allure.story("User Login")
class TestUserLogin:
    @allure.title("Check login as user")
    async def test_user_login(
        self, user: UserResponseDto, auth_client: AuthClient
    ) -> None:
        with allure.step("Send POST /auth/login request"):
            request = LoginRequestDto(email=user.email, password=user.password)
            response = await auth_client.login(request)

        with allure.step("Check login response"):
            assert response.status_code == HTTPStatus.CREATED
            TokensResponseDto.model_validate_json(response.content)

    @allure.title("Check invalid user login: {param_id}")
    @pytest.mark.parametrize(
        "request_dto",
        [
            pytest.param(
                LoginRequestDto(email="invalid", password="123123"),
                id="non email as email field value",
            ),
            pytest.param(
                LoginRequestDto(
                    email=f"invalid{uuid4().hex}@test.com", password="123123"
                ),
                id="non-existent email value",
            ),
            pytest.param(
                LoginRequestDto(email=None, password="123123"),
                id="email field is null",
            ),
            pytest.param(
                LoginRequestDto(email="john@mail.com", password=None),
                id="password field is null",
            ),
        ],
    )
    async def test_non_existent_user_login(
        self, auth_client: AuthClient, request_dto: LoginRequestDto
    ) -> None:
        with allure.step("Send POST /auth/login request"):
            request = LoginRequestDto(
                email=request_dto.email, password=request_dto.password
            )
            response = await auth_client.login(request)

        with allure.step("Check login response"):
            assert_unauthorized_error(response)
