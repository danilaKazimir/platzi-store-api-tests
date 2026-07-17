from http import HTTPStatus

import pytest

from src.clients.users_client import UsersClient
from src.models.users import UserResponseDto
from src.utils.assertions.users_assertions import assert_user_not_found


@pytest.mark.anyio
class TestDeleteUsers:
    NOT_FOUND_USER_ID = 0

    async def test_delete_user(
        self, user: UserResponseDto, users_client: UsersClient
    ) -> None:
        response = await users_client.delete_user(user.id)
        assert response.status_code == HTTPStatus.OK
        assert response.json() is True

        get_response = await users_client.get_single_user(user.id)
        assert_user_not_found(get_response)

    async def test_delete_non_existent_user(self, users_client: UsersClient) -> None:
        response = await users_client.delete_user(self.NOT_FOUND_USER_ID)
        assert_user_not_found(response)
