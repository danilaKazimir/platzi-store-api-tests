from http import HTTPStatus

import allure
import pytest

from src.clients.users_client import UsersClient
from src.models.users import UserResponseDto
from src.utils.assertions import assert_entity_not_found


@pytest.mark.anyio
@allure.parent_suite("API Tests")
@allure.suite("Users")
@allure.sub_suite("Delete Users")
@allure.feature("Users")
@allure.story("Delete User")
class TestDeleteUsers:
    NOT_FOUND_USER_ID = 0

    @allure.title("Check an existing user deletion")
    async def test_delete_user(
        self, user: UserResponseDto, users_client: UsersClient
    ) -> None:
        with allure.step("Send DELETE /users to delete user"):
            response = await users_client.delete_user(user.id)
            assert response.status_code == HTTPStatus.OK
            assert response.json() is True

        with allure.step("Check that user is deleted via GET /users"):
            get_response = await users_client.get_single_user(user.id)
            assert_entity_not_found(get_response)

    @allure.title("Check a non-existing user deletion")
    async def test_delete_non_existent_user(self, users_client: UsersClient) -> None:
        with allure.step("Send DELETE /users for non-existing user"):
            response = await users_client.delete_user(self.NOT_FOUND_USER_ID)
            assert_entity_not_found(response)
