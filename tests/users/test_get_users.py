from http import HTTPStatus

import pytest

from src.clients.users_client import UsersClient
from src.models.users import CreateUser, UserResponse, UsersResponse


@pytest.mark.anyio
class TestGetUsers:
    async def test_get_all_users(self, users_client: UsersClient) -> None:
        response = await users_client.get_all_users()

        assert response.status_code == HTTPStatus.OK
        assert all(
            isinstance(user, UserResponse)
            for user in UsersResponse.model_validate_json(response.content)
        )

    async def test_get_single_user(self, users_client: UsersClient) -> None:
        request: CreateUser = CreateUser(
            name="Ivan",
            email="ivanivanov@test.com",
            password="12345678",
            avatar="https://picsum.photos/800",
        )
        create_user_response = await users_client.create_user(request)
        created_user_response_model = UserResponse.model_validate_json(
            create_user_response.content
        )

        get_response = await users_client.get_single_user(
            created_user_response_model.id
        )
        assert get_response.status_code == HTTPStatus.OK

        get_user_response_model = UserResponse.model_validate_json(get_response.content)
        assert created_user_response_model == get_user_response_model
