from http import HTTPStatus

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
@allure.sub_suite("Retrieving User Profile")
@allure.feature("Auth")
@allure.story("Retrieving User Profile")
class TestRetrievingUserProfile:
    @allure.title("Check retrieving user profile")
    async def test_retrieving_user_profile(
        self, user: UserResponseDto, auth_client: AuthClient
    ) -> None:
        with allure.step("Getting access token after user login"):
            login_request = LoginRequestDto(email=user.email, password=user.password)
            login_response = await auth_client.login(login_request)
            access_token = TokensResponseDto.model_validate_json(
                login_response.content
            ).access_token

        with allure.step("Send GET /auth/profile request"):
            user_response = await auth_client.retrieving_user_profile(access_token)

        with allure.step("Check response"):
            assert user_response.status_code == HTTPStatus.OK
            user_response_model = UserResponseDto.model_validate_json(
                user_response.content
            )
            assert user == user_response_model

    @allure.title("Check invalid retrieving user profile: ")
    @pytest.mark.parametrize(
        "header",
        [
            pytest.param("invalid-token", id="with invalid token"),
            pytest.param(None, id="without token"),
        ],
    )
    async def test_invalid_retrieving_user_profile(
        self, header: str, auth_client: AuthClient
    ) -> None:
        with allure.step("Send GET /auth/profile request"):
            response = await auth_client.retrieving_user_profile(header)

        with allure.step("Check response"):
            assert_unauthorized_error(response)
