from http import HTTPStatus

import allure
import pytest

from src.clients.auth_client import AuthClient
from src.models.auth import LoginRequestDto, TokensResponseDto
from src.models.users import UserResponseDto


@pytest.mark.anyio
@allure.tag("api", "auth")
@allure.parent_suite("API Tests")
@allure.suite("Auth")
@allure.sub_suite("Refreshing Access Token")
@allure.feature("Auth")
@allure.story("Refreshing Access Token")
class TestRefreshingAccessToken:
    @allure.title("Check refresh access token")
    async def test_refresh_access_token(
        self, user: UserResponseDto, auth_client: AuthClient
    ) -> None:
        with allure.step("Getting refresh token after user login"):
            login_request = LoginRequestDto(email=user.email, password=user.password)
            login_response = await auth_client.login(login_request)
            refresh_token = TokensResponseDto.model_validate_json(
                login_response.content
            ).refresh_token

        with allure.step("Send GET /auth/refresh-token request"):
            refresh_response = await auth_client.refresh_token(refresh_token)

        with allure.step("Check GET /auth/refresh-token response"):
            assert refresh_response.status_code == HTTPStatus.CREATED
            new_access_token = TokensResponseDto.model_validate_json(
                refresh_response.content
            ).access_token

        with allure.step("Send GET /auth/refresh-token request"):
            retrieving_user_response = await auth_client.retrieving_user_profile(
                new_access_token
            )

        with allure.step("Check GET /auth/refresh-token response"):
            assert retrieving_user_response.status_code == HTTPStatus.OK
            user_response_model = UserResponseDto.model_validate_json(
                retrieving_user_response.content
            )
            assert user == user_response_model
