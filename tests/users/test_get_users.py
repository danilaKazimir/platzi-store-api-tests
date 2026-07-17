from http import HTTPStatus

import pytest

from src.clients.users_client import UsersClient
from src.models.users import UserResponseDto, UsersResponseDto
from src.utils.assertions.users_assertions import assert_user_not_found


@pytest.mark.anyio
class TestGetUsers:
    NOT_FOUND_USER_ID = 0

    async def test_get_all_users(self, users_client: UsersClient) -> None:
        response = await users_client.get_all_users()
        assert response.status_code == HTTPStatus.OK

        users = UsersResponseDto.model_validate_json(response.content)
        assert users.root

    async def test_get_single_user(
        self,
        user: UserResponseDto,
        users_client: UsersClient,
    ) -> None:
        response = await users_client.get_single_user(user.id)
        assert response.status_code == HTTPStatus.OK

        received_user = UserResponseDto.model_validate_json(response.content)
        assert received_user == user

    async def test_get_non_existent_user(self, users_client: UsersClient) -> None:
        response = await users_client.get_single_user(self.NOT_FOUND_USER_ID)
        assert_user_not_found(response)
