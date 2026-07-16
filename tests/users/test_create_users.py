from http import HTTPStatus

import pytest

from src.clients.users_client import UsersClient
from src.models.users import CreateUser, UserResponse


@pytest.mark.anyio
class TestCreateUsers:
    async def test_create_user(self, users_client: UsersClient) -> None:
        request: CreateUser = CreateUser(
            name="Ivan",
            email="ivanivanov@test.com",
            password="12345678",
            avatar="https://picsum.photos/800",
        )
        response = await users_client.create_user(request)
        assert response.status_code == HTTPStatus.CREATED

        response_model = UserResponse.model_validate_json(response.content)

        assert response_model.name == request.name
        assert response_model.email == request.email
        assert response_model.password == request.password
        assert response_model.avatar == request.avatar
