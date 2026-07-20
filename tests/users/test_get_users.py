from http import HTTPStatus

import allure
import pytest

from src.clients.users_client import UsersClient
from src.models.users import UserResponseDto, UsersResponseDto
from src.utils.assertions import assert_entity_not_found


@pytest.mark.anyio
@allure.feature("Users")
@allure.story("Get Users")
class TestGetUsers:
    NOT_FOUND_USER_ID = 0

    @allure.title("Check get list of all users")
    async def test_get_all_users(self, users_client: UsersClient) -> None:
        with allure.step("Send GET /users to get all users"):
            response = await users_client.get_all_users()
            assert response.status_code == HTTPStatus.OK

        with allure.step("Check GET /users response"):
            users = UsersResponseDto.model_validate_json(response.content)
            assert users.root

    @allure.title("Check get user information")
    async def test_get_single_user(
        self,
        user: UserResponseDto,
        users_client: UsersClient,
    ) -> None:
        with allure.step(f"Send GET /users/{user.id} to get user"):
            response = await users_client.get_single_user(user.id)
            assert response.status_code == HTTPStatus.OK

        with allure.step("Check GET /users response"):
            received_user = UserResponseDto.model_validate_json(response.content)
            assert received_user == user

    @allure.title("Check get a non-existing user ")
    async def test_get_non_existent_user(self, users_client: UsersClient) -> None:
        with allure.step(
            f"Send GET /users/{self.NOT_FOUND_USER_ID} for a non-existing user"
        ):
            response = await users_client.get_single_user(self.NOT_FOUND_USER_ID)
            assert_entity_not_found(response)
